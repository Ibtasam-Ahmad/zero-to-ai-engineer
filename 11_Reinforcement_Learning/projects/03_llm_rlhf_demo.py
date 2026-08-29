"""
RLHF Pipeline Demo Reward Model + PPO-style Policy Optimization
Demonstrates: Supervised Fine-Tuning → Reward Model → PPO conceptually
Requirements: torch transformers datasets trl peft
Usage:
  python 03_llm_rlhf_demo.py --stage reward_model   # Train reward model
  python 03_llm_rlhf_demo.py --stage ppo            # Run PPO fine-tuning
  python 03_llm_rlhf_demo.py --stage demo           # Demo all concepts
  python 03_llm_rlhf_demo.py --stage full           # Full RLHF pipeline
"""

import argparse
import json
import random
from dataclasses import dataclass
from typing import List, Tuple

# ── Preference Data ───────────────────────────────────────────────────────────
# In real RLHF, humans label (prompt, chosen, rejected) pairs.
# Here we simulate this with hand-crafted preference data.

PREFERENCE_DATA = [
    {
        "prompt": "Explain quantum computing in simple terms",
        "chosen": "Quantum computing uses quantum bits (qubits) that can be 0, 1, or both simultaneously through superposition. Unlike classical bits, this allows quantum computers to process many possibilities at once, making them powerful for specific tasks like cryptography and drug discovery.",
        "rejected": "Quantum computing is very complex and hard to explain. It uses quantum mechanics which is advanced physics.",
    },
    {
        "prompt": "What is machine learning?",
        "chosen": "Machine learning is a type of AI where computers learn from data rather than explicit programming. For example, instead of writing rules to detect spam, you show the system thousands of spam and non-spam emails, and it learns the patterns automatically.",
        "rejected": "Machine learning is when machines learn. It's a subset of artificial intelligence.",
    },
    {
        "prompt": "How do I stay healthy?",
        "chosen": "Key habits for good health: (1) Exercise 150 minutes/week of moderate activity, (2) Sleep 7-9 hours nightly, (3) Eat plenty of vegetables, fruits, and whole grains, (4) Stay hydrated, (5) Manage stress through meditation or social connection, (6) Schedule regular check-ups.",
        "rejected": "Just eat healthy and exercise. Also sleep enough and don't stress.",
    },
    {
        "prompt": "Explain gradient descent",
        "chosen": "Gradient descent minimizes a loss function by iteratively updating parameters in the direction of steepest decrease. Imagine a ball rolling downhill it always moves toward the lowest point. The learning rate controls step size; too large overshoots, too small converges slowly. Variants include SGD, Adam, and RMSprop.",
        "rejected": "Gradient descent is an optimization algorithm used in machine learning.",
    },
    {
        "prompt": "What is overfitting?",
        "chosen": "Overfitting occurs when a model memorizes training data instead of learning general patterns. It performs well on training data but poorly on unseen data. Think of a student who memorizes textbook answers but can't solve novel problems. Solutions include regularization (L1/L2), dropout, more training data, and cross-validation.",
        "rejected": "Overfitting is when your model is too complex and fits the training data too well.",
    },
    {
        "prompt": "Explain the attention mechanism",
        "chosen": "Attention allows models to focus on relevant parts of input when producing each output token. For each position, it computes Query, Key, Value vectors. Attention scores = softmax(QK^T / √d_k)V. This lets the model dynamically weight all input positions, solving the long-range dependency problem of RNNs.",
        "rejected": "Attention is a mechanism in transformers that helps the model pay attention to important parts.",
    },
]

# ── Reward Model (Classifier) ─────────────────────────────────────────────────

@dataclass
class RewardModelOutput:
    score: float
    chosen_score: float
    rejected_score: float
    preference_correct: bool

class SimpleRewardModel:
    """
    Simple reward model based on response quality heuristics.
    In production: fine-tune a language model (e.g. GPT-2 with a classification head)
    on (chosen, rejected) pairs using the Bradley-Terry model.
    """
    def score(self, prompt: str, response: str) -> float:
        """Score a response higher is better."""
        score = 0.0
        # Length heuristic too short is bad
        words = response.split()
        if len(words) > 30:
            score += 0.2
        if len(words) > 60:
            score += 0.2
        # Specificity contains numbers, lists
        if any(c.isdigit() for c in response):
            score += 0.15
        if any(marker in response for marker in ["(1)", "(2)", "1.", "2.", "•", "-"]):
            score += 0.1
        # Concrete examples
        if any(w in response.lower() for w in ["example", "for instance", "such as", "like"]):
            score += 0.1
        # Explanatory depth
        if any(w in response.lower() for w in ["because", "therefore", "which means", "this allows"]):
            score += 0.15
        # Penalize vague language
        if response.count("very") + response.count("really") + response.count("just") > 3:
            score -= 0.1
        return min(1.0, max(0.0, score))

    def compare(self, prompt: str, chosen: str, rejected: str) -> RewardModelOutput:
        cs = self.score(prompt, chosen)
        rs = self.score(prompt, rejected)
        return RewardModelOutput(
            score=cs - rs,
            chosen_score=cs,
            rejected_score=rs,
            preference_correct=cs > rs,
        )

def train_reward_model():
    """Demonstrate reward model training and evaluation."""
    print("=" * 60)
    print("STAGE 1: REWARD MODEL TRAINING")
    print("=" * 60)
    print("\nUsing preference data with (prompt, chosen, rejected) pairs.")
    print("Loss function: -log(σ(r_chosen - r_rejected)) [Bradley-Terry model]\n")

    rm = SimpleRewardModel()
    correct = 0

    for i, pref in enumerate(PREFERENCE_DATA):
        out = rm.compare(pref["prompt"], pref["chosen"], pref["rejected"])
        status = "✓" if out.preference_correct else "✗"
        print(f"  {status} [{i+1}] {pref['prompt'][:45]:<45} | "
              f"chosen={out.chosen_score:.2f} rejected={out.rejected_score:.2f} Δ={out.score:+.2f}")
        if out.preference_correct:
            correct += 1

    acc = correct / len(PREFERENCE_DATA)
    print(f"\nReward Model Accuracy: {correct}/{len(PREFERENCE_DATA)} = {acc:.1%}")
    print("(In practice: fine-tune a pre-trained LM with a reward head on ~10k+ preference pairs)")
    return rm

# ── PPO Conceptual Demo ───────────────────────────────────────────────────────

@dataclass
class PPOStep:
    prompt: str
    response: str
    reward: float
    kl_penalty: float
    clipped_ratio: float
    policy_loss: float

def ppo_demo(rm: SimpleRewardModel, episodes: int = 20):
    """
    Conceptual PPO demonstration. Shows the key equations:
    - PPO clipped objective: L_CLIP = E[min(r_t*A_t, clip(r_t, 1-ε, 1+ε)*A_t)]
    - KL penalty: L_KL = β * KL(π_θ || π_ref)
    - Total loss: L = L_CLIP - c1*L_VF + c2*S[π_θ]
    """
    print("\n" + "=" * 60)
    print("STAGE 2: PPO FINE-TUNING")
    print("=" * 60)
    print("\nKey PPO equations:")
    print("  L_CLIP = E[min(r_t·A_t, clip(r_t, 1-ε, 1+ε)·A_t)]")
    print("  KL penalty: β·KL(π_θ || π_ref)")
    print("  Total: L_CLIP - c1·L_VF + c2·entropy_bonus\n")

    prompts = [p["prompt"] for p in PREFERENCE_DATA]
    responses_pool = [p["chosen"] for p in PREFERENCE_DATA] + [p["rejected"] for p in PREFERENCE_DATA]

    # Simulate reward improvement over PPO steps
    rewards_history = []
    beta = 0.1  # KL penalty coefficient
    epsilon = 0.2  # PPO clip range
    base_reward = 0.45  # Starting point

    steps = []
    for ep in range(episodes):
        prompt = prompts[ep % len(prompts)]
        # Simulate improving policy: reward trends upward with noise
        improvement = ep * 0.015
        reward = min(0.85, base_reward + improvement + random.gauss(0, 0.05))

        # Simulate KL divergence (grows as policy diverges from reference)
        kl_penalty = beta * (0.05 + ep * 0.003 + random.gauss(0, 0.01))

        # Simulate advantage estimate
        advantage = reward - 0.5  # baseline = 0.5

        # Simulate clipping: ratio near 1.0 early, drifting later
        ratio = 1.0 + random.gauss(0, 0.1) + ep * 0.005
        clipped_ratio = max(1 - epsilon, min(1 + epsilon, ratio))
        policy_loss = -min(ratio * advantage, clipped_ratio * advantage) + kl_penalty

        rewards_history.append(reward)
        steps.append(PPOStep(prompt, "", reward, kl_penalty, clipped_ratio, policy_loss))

        if ep % 5 == 0:
            avg_r = sum(rewards_history[-5:]) / min(5, len(rewards_history))
            print(f"  Step {ep+1:>3} | Reward: {reward:.3f} | KL: {kl_penalty:.3f} | "
                  f"Clip ratio: {clipped_ratio:.3f} | Loss: {policy_loss:.4f} | Avg(5): {avg_r:.3f}")

    final_avg = sum(rewards_history[-5:]) / 5
    initial_avg = sum(rewards_history[:5]) / 5
    print(f"\nReward improvement: {initial_avg:.3f} → {final_avg:.3f} (+{final_avg-initial_avg:.3f})")
    return rewards_history

# ── RLHF Full Pipeline Summary ────────────────────────────────────────────────

def print_rlhf_pipeline():
    print("\n" + "=" * 60)
    print("RLHF PIPELINE OVERVIEW")
    print("=" * 60)

    stages = [
        ("Stage 1: SFT (Supervised Fine-Tuning)",
         "Fine-tune a pretrained LLM on high-quality (prompt, response) pairs.\n"
         "  Loss: L_SFT = -Σ log P(y_t | x, y_{<t})  [standard LM cross-entropy]"),
        ("Stage 2: Reward Model (RM)",
         "Train RM to predict human preferences from (chosen, rejected) pairs.\n"
         "  Loss: L_RM = -E[log σ(r_θ(x, y_c) - r_θ(x, y_r))]  [Bradley-Terry]"),
        ("Stage 3: PPO (Proximal Policy Optimization)",
         "Fine-tune SFT model using RM as reward signal, with KL constraint.\n"
         "  Reward: r(x,y) = r_θ(x,y) - β·KL(π_φ(y|x) || π_ref(y|x))\n"
         "  L_PPO = E[min(r_t·A_t, clip(r_t, 1-ε, 1+ε)·A_t)]"),
        ("Alternatives to PPO",
         "• DPO (Direct Preference Optimization): bypasses RM entirely.\n"
         "  L_DPO = -E[log σ(β·log π_θ(y_c|x)/π_ref(y_c|x) - β·log π_θ(y_r|x)/π_ref(y_r|x))]\n"
         "• RLAIF: Use AI feedback instead of human feedback (Claude as judge)\n"
         "• KTO: Kahneman-Tversky Optimization uses binary feedback (good/bad)"),
    ]

    for title, detail in stages:
        print(f"\n{'─'*50}")
        print(f"  {title}")
        print(f"  {detail}")

    print("\n" + "─" * 50)
    print("\nKey libraries for production RLHF:")
    print("  • TRL (HuggingFace): PPOTrainer, DPOTrainer, RewardTrainer")
    print("  • OpenRLHF: scalable RLHF with Ray + DeepSpeed")
    print("  • Unsloth: 2x faster RLHF training")
    print("  • vLLM: fast inference during rollout generation")

def plot_rlhf(rewards_history: List[float]):
    try:
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        # Reward over PPO steps
        ax = axes[0]
        ax.plot(rewards_history, "b-", alpha=0.5, label="Episode reward")
        window = 5
        if len(rewards_history) >= window:
            avg = [sum(rewards_history[i:i+window])/window for i in range(len(rewards_history)-window+1)]
            ax.plot(range(window-1, len(rewards_history)), avg, "r-", linewidth=2, label=f"Moving avg ({window})")
        ax.set_title("PPO Reward Over Training Steps")
        ax.set_xlabel("PPO Step")
        ax.set_ylabel("Reward")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Reward model scores: chosen vs rejected
        ax = axes[1]
        rm = SimpleRewardModel()
        chosen_scores = [rm.score(p["prompt"], p["chosen"]) for p in PREFERENCE_DATA]
        rejected_scores = [rm.score(p["prompt"], p["rejected"]) for p in PREFERENCE_DATA]
        x = range(len(PREFERENCE_DATA))
        ax.bar([i - 0.2 for i in x], chosen_scores, 0.4, label="Chosen", color="green", alpha=0.7)
        ax.bar([i + 0.2 for i in x], rejected_scores, 0.4, label="Rejected", color="red", alpha=0.7)
        ax.set_title("Reward Model: Chosen vs Rejected")
        ax.set_xlabel("Sample")
        ax.set_ylabel("Reward Score")
        ax.legend()
        ax.grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        plt.savefig("rlhf_demo.png", dpi=100)
        print("\nPlot saved to rlhf_demo.png")
        plt.show()
    except Exception as e:
        print(f"Plot skipped: {e}")

# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RLHF Pipeline Demo")
    parser.add_argument("--stage", default="demo",
                        choices=["reward_model", "ppo", "demo", "full"])
    parser.add_argument("--episodes", type=int, default=20)
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()

    print("RLHF (Reinforcement Learning from Human Feedback) Demo")
    print("This script demonstrates the three stages conceptually.\n")

    if args.stage in ("reward_model", "full"):
        rm = train_reward_model()

    if args.stage in ("ppo", "full"):
        if args.stage == "ppo":
            rm = SimpleRewardModel()
        rewards = ppo_demo(rm, episodes=args.episodes)
        if args.plot:
            plot_rlhf(rewards)

    if args.stage in ("demo", "full"):
        rm = train_reward_model()
        rewards = ppo_demo(rm, episodes=args.episodes)
        print_rlhf_pipeline()
        if args.plot:
            plot_rlhf(rewards)
