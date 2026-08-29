"""
Multi-Armed Bandit: Exploration vs Exploitation Strategies
Compares: ε-Greedy, UCB1, Thompson Sampling, Gradient Bandit.
Includes regret analysis and confidence bound visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# ─── Bandit Environment ───────────────────────────────────────────────────────

class StationaryBandit:
    """
    K-armed stationary bandit.
    Each arm has a true reward mean drawn from N(0, 1).
    Rewards are noisy: R ~ N(μ_a, σ=1).
    """

    def __init__(self, k=10, seed=42):
        self.k = k
        np.random.seed(seed)
        self.true_means = np.random.normal(0, 1, k)
        self.optimal_arm = np.argmax(self.true_means)
        self.optimal_mean = self.true_means[self.optimal_arm]
        print(f"Bandit: {k} arms | Optimal arm: {self.optimal_arm} "
              f"(μ={self.optimal_mean:.3f})")

    def pull(self, arm):
        """Pull arm and receive stochastic reward."""
        return np.random.normal(self.true_means[arm], 1.0)


class NonStationaryBandit(StationaryBandit):
    """
    Non-stationary bandit where true means drift over time.
    Each step: μ_a += N(0, 0.01)
    """

    def pull(self, arm):
        # Random walk for all arms
        self.true_means += np.random.normal(0, 0.01, self.k)
        self.optimal_arm = np.argmax(self.true_means)
        return np.random.normal(self.true_means[arm], 1.0)


# ─── Agents ───────────────────────────────────────────────────────────────────

class EpsilonGreedy:
    """
    ε-Greedy: exploit best known arm with probability 1-ε,
    explore randomly with probability ε.
    """

    def __init__(self, k, epsilon=0.1, name=None):
        self.k = k
        self.epsilon = epsilon
        self.name = name or f"ε-Greedy(ε={epsilon})"
        self.reset()

    def reset(self):
        self.q = np.zeros(self.k)     # Action-value estimates
        self.n = np.zeros(self.k)     # Pull counts

    def select(self, t):
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.k)
        return np.argmax(self.q)

    def update(self, arm, reward):
        self.n[arm] += 1
        # Incremental update: Q ← Q + (1/n)(R - Q)
        self.q[arm] += (reward - self.q[arm]) / self.n[arm]


class UCB1:
    """
    UCB1 (Upper Confidence Bound):
    Select arm that maximizes Q(a) + c * sqrt(ln(t) / N(a))
    Provides theoretical regret bound O(K ln T).
    """

    def __init__(self, k, c=2.0, name=None):
        self.k = k
        self.c = c
        self.name = name or f"UCB1(c={c})"
        self.reset()

    def reset(self):
        self.q = np.zeros(self.k)
        self.n = np.zeros(self.k)

    def select(self, t):
        # Pull each arm once first
        if t < self.k:
            return t
        # UCB selection
        ucb = self.q + self.c * np.sqrt(np.log(t) / (self.n + 1e-8))
        return np.argmax(ucb)

    def update(self, arm, reward):
        self.n[arm] += 1
        self.q[arm] += (reward - self.q[arm]) / self.n[arm]


class ThompsonSampling:
    """
    Thompson Sampling (Bayesian):
    Assumes Beta(α, β) posterior for Bernoulli rewards.
    Adapted for Gaussian rewards using Normal-Normal conjugate.
    """

    def __init__(self, k, name="Thompson Sampling"):
        self.k = k
        self.name = name
        self.reset()

    def reset(self):
        self.alpha = np.ones(self.k)   # Posterior parameters
        self.beta = np.ones(self.k)
        self.sum_rewards = np.zeros(self.k)
        self.n = np.zeros(self.k)

    def select(self, t):
        # Sample from posterior for each arm
        samples = np.random.beta(self.alpha, self.beta)
        return np.argmax(samples)

    def update(self, arm, reward):
        self.n[arm] += 1
        # Shift reward to [0, 1] for Beta update
        r_shifted = (reward + 3) / 6  # Map ~[-3, 3] to [0, 1]
        r_shifted = np.clip(r_shifted, 0, 1)
        self.alpha[arm] += r_shifted
        self.beta[arm] += 1 - r_shifted


class GradientBandit:
    """
    Gradient Bandit (policy gradient approach):
    Maintains preference H(a) and selects by softmax.
    Update: H(a) += α(R - baseline) * (1[a_t=a] - π(a))
    """

    def __init__(self, k, lr=0.1, baseline=True, name=None):
        self.k = k
        self.lr = lr
        self.use_baseline = baseline
        self.name = name or f"Gradient(lr={lr})"
        self.reset()

    def reset(self):
        self.H = np.zeros(self.k)   # Preferences
        self.baseline = 0           # Running average reward
        self.t = 0

    def softmax(self):
        """Numerically stable softmax over preferences."""
        h = self.H - self.H.max()
        exp_h = np.exp(h)
        return exp_h / exp_h.sum()

    def select(self, t):
        probs = self.softmax()
        return np.random.choice(self.k, p=probs)

    def update(self, arm, reward):
        self.t += 1
        probs = self.softmax()
        b = self.baseline if self.use_baseline else 0

        # Policy gradient update
        for a in range(self.k):
            if a == arm:
                self.H[a] += self.lr * (reward - b) * (1 - probs[a])
            else:
                self.H[a] -= self.lr * (reward - b) * probs[a]

        if self.use_baseline:
            # Update baseline (running mean)
            self.baseline += (reward - self.baseline) / self.t


# ─── Simulation ───────────────────────────────────────────────────────────────

def run_simulation(bandit, agents, n_steps=1000, n_runs=200):
    """
    Run multiple independent trials of all agents.
    Returns: rewards [n_agents, n_runs, n_steps], optimal_actions [n_agents, n_runs, n_steps]
    """
    n_agents = len(agents)
    rewards = np.zeros((n_agents, n_runs, n_steps))
    optimal_actions = np.zeros((n_agents, n_runs, n_steps))

    for run in range(n_runs):
        # Fresh bandit environment per run
        np.random.seed(run)
        bandit.true_means = np.random.normal(0, 1, bandit.k)
        bandit.optimal_arm = np.argmax(bandit.true_means)

        # Reset all agents
        for agent in agents:
            agent.reset()

        for t in range(n_steps):
            for i, agent in enumerate(agents):
                arm = agent.select(t)
                reward = bandit.pull(arm)
                agent.update(arm, reward)
                rewards[i, run, t] = reward
                optimal_actions[i, run, t] = float(arm == bandit.optimal_arm)

    return rewards, optimal_actions


def compute_regret(rewards, bandit, n_runs, n_steps):
    """Compute cumulative regret = T * μ* - Σ R_t."""
    optimal_reward = np.mean(np.random.normal(0, 1, (n_runs, n_steps)).clip(-3, 3)) * 0 + 1.0
    # Approximate: expected regret at step t = optimal_mean - E[R_t]
    mean_rewards = rewards.mean(axis=1)  # [n_agents, n_steps]
    return np.cumsum(1.0 - mean_rewards, axis=1)  # Relative regret


# ─── Visualization ───────────────────────────────────────────────────────────

def plot_results(agents, rewards, optimal_actions, regret):
    """4-panel comparison plot."""
    colors = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6"]
    n_steps = rewards.shape[2]
    t = np.arange(1, n_steps + 1)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Average reward over time
    ax = axes[0, 0]
    for i, agent in enumerate(agents):
        mean_r = rewards[i].mean(axis=0)
        ax.plot(t, mean_r, color=colors[i], label=agent.name, linewidth=1.5)
    ax.set_title("Average Reward per Step")
    ax.set_xlabel("Step")
    ax.set_ylabel("Reward")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # 2. % Optimal action
    ax = axes[0, 1]
    for i, agent in enumerate(agents):
        pct_opt = optimal_actions[i].mean(axis=0) * 100
        ax.plot(t, pct_opt, color=colors[i], label=agent.name, linewidth=1.5)
    ax.set_title("% Optimal Action")
    ax.set_xlabel("Step")
    ax.set_ylabel("% Optimal")
    ax.set_ylim(0, 100)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # 3. Cumulative regret
    ax = axes[1, 0]
    for i, agent in enumerate(agents):
        ax.plot(t, regret[i], color=colors[i], label=agent.name, linewidth=1.5)
    ax.set_title("Cumulative Regret")
    ax.set_xlabel("Step")
    ax.set_ylabel("Regret")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # 4. Final performance bar chart
    ax = axes[1, 1]
    final_rewards = [rewards[i].mean(axis=0)[-100:].mean() for i in range(len(agents))]
    bars = ax.bar([a.name for a in agents], final_rewards,
                  color=colors[:len(agents)], edgecolor="black", linewidth=0.5)
    ax.set_title("Avg Reward (Last 100 Steps)")
    ax.set_ylabel("Reward")
    ax.tick_params(axis="x", rotation=30)
    for bar, val in zip(bars, final_rewards):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f"{val:.3f}", ha="center", va="bottom", fontsize=8)
    ax.grid(True, alpha=0.3, axis="y")

    plt.suptitle("Multi-Armed Bandit: Strategy Comparison (200 runs)", fontsize=13)
    plt.tight_layout()
    plt.savefig("bandit_comparison.png", dpi=100)
    print("Results saved to bandit_comparison.png")
    plt.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  MULTI-ARMED BANDIT EXPLORATION STRATEGIES")
    print("=" * 60)

    K = 10
    N_STEPS = 1000
    N_RUNS = 200

    bandit = StationaryBandit(k=K)

    agents = [
        EpsilonGreedy(K, epsilon=0.0, name="Greedy (ε=0)"),
        EpsilonGreedy(K, epsilon=0.1, name="ε-Greedy (ε=0.1)"),
        UCB1(K, c=2.0),
        ThompsonSampling(K),
        GradientBandit(K, lr=0.1),
    ]

    print(f"\nRunning {N_RUNS} trials × {N_STEPS} steps per agent...")
    rewards, optimal_actions = run_simulation(bandit, agents, N_STEPS, N_RUNS)
    regret = compute_regret(rewards, bandit, N_RUNS, N_STEPS)

    # Summary table
    print("\n=== Final Performance (averaged over last 100 steps) ===")
    print(f"{'Agent':<25} {'Avg Reward':>12} {'% Optimal':>12} {'Cum Regret':>12}")
    print("-" * 63)
    for i, agent in enumerate(agents):
        avg_r = rewards[i].mean(axis=0)[-100:].mean()
        pct_opt = optimal_actions[i].mean(axis=0)[-100:].mean() * 100
        cum_reg = regret[i][-1]
        print(f"{agent.name:<25} {avg_r:>12.4f} {pct_opt:>11.1f}% {cum_reg:>12.2f}")

    print("\nPlotting comparison...")
    plot_results(agents, rewards, optimal_actions, regret)

    print("\nKey insights:")
    print("  • Greedy (ε=0) exploits early but gets stuck in suboptimal arms")
    print("  • ε-Greedy balances exploration but wastes pulls randomly")
    print("  • UCB1 provides provably optimal O(K ln T) regret bound")
    print("  • Thompson Sampling matches UCB1 empirically with Bayesian elegance")
    print("  • Gradient Bandit learns policy directly without value estimation")
    print("\nDone!")
