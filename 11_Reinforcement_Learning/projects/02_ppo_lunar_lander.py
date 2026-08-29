"""
LunarLander-v2 solved with Proximal Policy Optimization (PPO)
From scratch: actor-critic, GAE advantage estimation, clipped objective.
Requirements: gymnasium torch numpy matplotlib
"""

import numpy as np
import time
import matplotlib.pyplot as plt
from collections import deque

import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical

try:
    import gymnasium as gym
    try:
        env_test = gym.make("LunarLander-v3")
        env_test.close()
        ENV_NAME = "LunarLander-v3"
    except Exception:
        ENV_NAME = "LunarLander-v2"
except ImportError:
    import gym
    ENV_NAME = "LunarLander-v2"

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {DEVICE} | Env: {ENV_NAME}")

# ─── Hyperparameters ──────────────────────────────────────────────────────────

LR_ACTOR = 3e-4
LR_CRITIC = 1e-3
GAMMA = 0.99
GAE_LAMBDA = 0.95
CLIP_EPS = 0.2          # PPO clipping parameter
ENTROPY_COEF = 0.01     # Encourage exploration
VALUE_COEF = 0.5        # Critic loss weight
EPOCHS = 4              # Update passes per rollout
ROLLOUT_STEPS = 2048    # Steps per policy rollout
MINI_BATCH = 64
MAX_STEPS = 1_000_000
SOLVED_THRESHOLD = 200  # Average reward over 100 episodes


# ─── Networks ─────────────────────────────────────────────────────────────────

class ActorCritic(nn.Module):
    """
    Shared backbone with separate actor (policy) and critic (value) heads.

    Actor:  π(a|s) = softmax(W_actor · φ(s))
    Critic: V(s) = W_critic · φ(s)
    """

    def __init__(self, state_dim, action_dim, hidden=256):
        super().__init__()
        self.backbone = nn.Sequential(
            nn.Linear(state_dim, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
        )
        self.actor_head = nn.Linear(hidden, action_dim)
        self.critic_head = nn.Linear(hidden, 1)

        # Orthogonal initialization
        for layer in self.backbone:
            if isinstance(layer, nn.Linear):
                nn.init.orthogonal_(layer.weight, gain=np.sqrt(2))
                nn.init.constant_(layer.bias, 0)
        nn.init.orthogonal_(self.actor_head.weight, gain=0.01)
        nn.init.orthogonal_(self.critic_head.weight, gain=1.0)

    def forward(self, x):
        feat = self.backbone(x)
        logits = self.actor_head(feat)
        value = self.critic_head(feat).squeeze(-1)
        return logits, value

    def get_action(self, state):
        logits, value = self(state)
        dist = Categorical(logits=logits)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        entropy = dist.entropy()
        return action, log_prob, value, entropy


# ─── Rollout Buffer ───────────────────────────────────────────────────────────

class RolloutBuffer:
    """Stores a single rollout for PPO updates."""

    def __init__(self):
        self.clear()

    def clear(self):
        self.states = []
        self.actions = []
        self.log_probs = []
        self.rewards = []
        self.values = []
        self.dones = []

    def add(self, state, action, log_prob, reward, value, done):
        self.states.append(state)
        self.actions.append(action)
        self.log_probs.append(log_prob)
        self.rewards.append(reward)
        self.values.append(value)
        self.dones.append(done)

    def compute_gae(self, last_value, gamma=GAMMA, lam=GAE_LAMBDA):
        """
        Generalized Advantage Estimation (GAE):
        A_t = Σ_{l=0}^{T-t} (γλ)^l δ_{t+l}
        where δ_t = r_t + γV(s_{t+1}) - V(s_t)
        """
        rewards = np.array(self.rewards)
        values = np.array([v.item() for v in self.values])
        dones = np.array(self.dones)

        advantages = np.zeros_like(rewards)
        gae = 0

        for t in reversed(range(len(rewards))):
            next_val = last_value if t == len(rewards) - 1 else values[t + 1]
            next_done = 0 if t == len(rewards) - 1 else dones[t + 1]
            delta = rewards[t] + gamma * next_val * (1 - next_done) - values[t]
            gae = delta + gamma * lam * (1 - next_done) * gae
            advantages[t] = gae

        returns = advantages + values
        return advantages, returns

    def to_tensors(self, advantages, returns):
        states = torch.FloatTensor(np.array(self.states)).to(DEVICE)
        actions = torch.LongTensor(self.actions).to(DEVICE)
        old_log_probs = torch.FloatTensor(self.log_probs).to(DEVICE)
        advantages_t = torch.FloatTensor(advantages).to(DEVICE)
        returns_t = torch.FloatTensor(returns).to(DEVICE)
        # Normalize advantages
        advantages_t = (advantages_t - advantages_t.mean()) / (advantages_t.std() + 1e-8)
        return states, actions, old_log_probs, advantages_t, returns_t


# ─── PPO Update ───────────────────────────────────────────────────────────────

def ppo_update(model, optimizer, buffer, last_value):
    """
    PPO clipped objective:
    L^CLIP = E[min(r_t * A_t, clip(r_t, 1-ε, 1+ε) * A_t)]
    where r_t = π(a|s) / π_old(a|s)
    """
    advantages, returns = buffer.compute_gae(last_value)
    states, actions, old_log_probs, adv, ret = buffer.to_tensors(advantages, returns)
    n = len(states)

    pg_losses, v_losses, entropy_losses = [], [], []

    for _ in range(EPOCHS):
        # Mini-batch updates
        indices = torch.randperm(n)
        for start in range(0, n, MINI_BATCH):
            idx = indices[start:start + MINI_BATCH]
            b_states = states[idx]
            b_actions = actions[idx]
            b_old_log_probs = old_log_probs[idx]
            b_adv = adv[idx]
            b_ret = ret[idx]

            logits, values = model(b_states)
            dist = Categorical(logits=logits)
            new_log_probs = dist.log_prob(b_actions)
            entropy = dist.entropy().mean()

            # Probability ratio: π_new / π_old
            ratio = (new_log_probs - b_old_log_probs).exp()

            # Clipped surrogate loss
            pg_loss1 = ratio * b_adv
            pg_loss2 = ratio.clamp(1 - CLIP_EPS, 1 + CLIP_EPS) * b_adv
            pg_loss = -torch.min(pg_loss1, pg_loss2).mean()

            # Value loss
            v_loss = ((values - b_ret) ** 2).mean()

            # Total loss
            loss = pg_loss + VALUE_COEF * v_loss - ENTROPY_COEF * entropy

            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 0.5)
            optimizer.step()

            pg_losses.append(pg_loss.item())
            v_losses.append(v_loss.item())
            entropy_losses.append(entropy.item())

    return np.mean(pg_losses), np.mean(v_losses), np.mean(entropy_losses)


# ─── Training ─────────────────────────────────────────────────────────────────

def train():
    env = gym.make(ENV_NAME)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n
    print(f"State: {state_dim}D | Actions: {action_dim}")

    model = ActorCritic(state_dim, action_dim).to(DEVICE)
    optimizer = optim.Adam(model.parameters(), lr=LR_ACTOR, eps=1e-5)
    buffer = RolloutBuffer()

    result = env.reset()
    state = result[0] if isinstance(result, tuple) else result
    state = np.array(state, dtype=np.float32)

    episode_rewards = []
    current_ep_reward = 0
    solved_at = None
    total_steps = 0
    update_count = 0

    print(f"\nTraining for up to {MAX_STEPS:,} steps...")
    t0 = time.time()

    while total_steps < MAX_STEPS:
        # Collect rollout
        for _ in range(ROLLOUT_STEPS):
            state_t = torch.FloatTensor(state).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                action, log_prob, value, _ = model.get_action(state_t)

            result = env.step(action.item())
            if len(result) == 5:
                next_state, reward, terminated, truncated, _ = result
                done = terminated or truncated
            else:
                next_state, reward, done, _ = result

            buffer.add(state, action.item(), log_prob.item(), reward, value, float(done))
            state = np.array(next_state, dtype=np.float32)
            current_ep_reward += reward
            total_steps += 1

            if done:
                episode_rewards.append(current_ep_reward)
                current_ep_reward = 0
                result = env.reset()
                state = np.array(result[0] if isinstance(result, tuple) else result,
                                 dtype=np.float32)

        # Get value estimate for last state
        with torch.no_grad():
            last_val_t = torch.FloatTensor(state).unsqueeze(0).to(DEVICE)
            _, last_value, _, _ = model.get_action(last_val_t)
            last_value = last_value.item()

        pg_loss, v_loss, entropy = ppo_update(model, optimizer, buffer, last_value)
        buffer.clear()
        update_count += 1

        if len(episode_rewards) >= 10 and update_count % 5 == 0:
            avg_100 = np.mean(episode_rewards[-100:])
            n_eps = len(episode_rewards)
            elapsed = time.time() - t0
            print(f"Steps: {total_steps:7d} | Eps: {n_eps:4d} | "
                  f"Avg(100): {avg_100:7.2f} | PG: {pg_loss:.4f} | "
                  f"V: {v_loss:.4f} | {elapsed:.0f}s")

            if avg_100 >= SOLVED_THRESHOLD and solved_at is None:
                solved_at = n_eps
                print(f"\nSOLVED at episode {n_eps}! Avg(100) = {avg_100:.2f}\n")

    env.close()
    return model, episode_rewards, solved_at


def plot_results(rewards, solved_at=None):
    plt.figure(figsize=(10, 4))
    plt.plot(rewards, alpha=0.3, color="#3498db", label="Episode Reward")
    if len(rewards) >= 100:
        rolling = [np.mean(rewards[max(0, i-100):i+1]) for i in range(len(rewards))]
        plt.plot(rolling, color="#e74c3c", linewidth=2, label="Avg(100)")
    plt.axhline(SOLVED_THRESHOLD, color="green", linestyle="--",
                linewidth=1.5, label=f"Solved ({SOLVED_THRESHOLD})")
    if solved_at:
        plt.axvline(solved_at, color="orange", linestyle="--", label=f"Solved at ep {solved_at}")
    plt.title(f"PPO Training on {ENV_NAME}", fontsize=13)
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("ppo_lunar_lander.png", dpi=100)
    print("Training plot saved to ppo_lunar_lander.png")
    plt.close()


if __name__ == "__main__":
    print("=" * 55)
    print(f"  PPO PROXIMAL POLICY OPTIMIZATION ({ENV_NAME})")
    print("=" * 55)

    model, rewards, solved_at = train()
    plot_results(rewards, solved_at)

    if rewards:
        print(f"\nFinal stats:")
        print(f"  Total episodes: {len(rewards)}")
        print(f"  Best avg(100):  {max(np.mean(rewards[max(0,i-100):i+1]) for i in range(len(rewards))):.2f}")
        print(f"  Solved at:      {solved_at or 'Not solved'}")
    print("\nDone!")
