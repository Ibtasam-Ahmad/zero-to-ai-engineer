"""
GridWorld RL Dynamic Programming, Monte Carlo, TD Learning (SARSA/Q-Learning)
No dependencies beyond Python standard library and numpy/matplotlib.
Usage:
  python 02_gridworld_rl.py --algo q_learning
  python 02_gridworld_rl.py --algo sarsa --episodes 2000
  python 02_gridworld_rl.py --algo policy_iteration --visualize
  python 02_gridworld_rl.py --compare  # Compare all algorithms
"""

import argparse
import random
from typing import Dict, List, Optional, Tuple

import numpy as np

# ── GridWorld Environment ─────────────────────────────────────────────────────

class GridWorld:
    """
    5x5 grid:
    S . . . .
    . X . X .
    . . . . .
    . X . X .
    . . . . G
    S=start(0,0), G=goal(4,4), X=walls, .=empty
    Rewards: +10 goal, -1 wall bump, -0.1 step
    """
    ACTIONS = [0, 1, 2, 3]  # up, down, left, right
    ACTION_NAMES = ["↑", "↓", "←", "→"]
    DELTAS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def __init__(self, size: int = 5):
        self.size = size
        self.walls = {(1, 1), (1, 3), (3, 1), (3, 3)}
        self.start = (0, 0)
        self.goal = (size - 1, size - 1)
        self.state = self.start
        self.n_states = size * size
        self.n_actions = 4

    def reset(self) -> Tuple[int, int]:
        self.state = self.start
        return self.state

    def step(self, action: int) -> Tuple[Tuple[int, int], float, bool]:
        r, c = self.state
        dr, dc = self.DELTAS[action]
        nr, nc = r + dr, c + dc

        # Boundary / wall check stay in place on invalid move
        if (0 <= nr < self.size and 0 <= nc < self.size and (nr, nc) not in self.walls):
            self.state = (nr, nc)
            reward = -0.1
        else:
            reward = -1.0  # penalty for bumping

        done = self.state == self.goal
        if done:
            reward = 10.0
        return self.state, reward, done

    def state_to_idx(self, s: Tuple[int, int]) -> int:
        return s[0] * self.size + s[1]

    def idx_to_state(self, idx: int) -> Tuple[int, int]:
        return divmod(idx, self.size)

    def is_terminal(self, s: Tuple[int, int]) -> bool:
        return s == self.goal

    def all_states(self) -> List[Tuple[int, int]]:
        return [(r, c) for r in range(self.size) for c in range(self.size) if (r, c) not in self.walls]

# ── Dynamic Programming ───────────────────────────────────────────────────────

def policy_iteration(env: GridWorld, gamma: float = 0.95, theta: float = 1e-6) -> Tuple[np.ndarray, np.ndarray, List[float]]:
    """Policy Iteration: policy evaluation + policy improvement alternation."""
    n = env.n_states
    V = np.zeros(n)
    # Random initial policy (action per non-wall state)
    policy = np.random.randint(0, 4, size=n)
    convergence = []

    def evaluate(max_iter=1000):
        for _ in range(max_iter):
            delta = 0
            for s_idx in range(n):
                s = env.idx_to_state(s_idx)
                if s in env.walls or env.is_terminal(s):
                    continue
                a = policy[s_idx]
                env.state = s
                ns, r, done = env.step(a)
                ns_idx = env.state_to_idx(ns)
                new_v = r + (0 if done else gamma * V[ns_idx])
                delta = max(delta, abs(new_v - V[s_idx]))
                V[s_idx] = new_v
                env.state = s
            convergence.append(delta)
            if delta < theta:
                break

    for _ in range(50):
        evaluate()
        stable = True
        for s_idx in range(n):
            s = env.idx_to_state(s_idx)
            if s in env.walls or env.is_terminal(s):
                continue
            best_a, best_v = 0, -1e9
            for a in range(4):
                env.state = s
                ns, r, done = env.step(a)
                ns_idx = env.state_to_idx(ns)
                v = r + (0 if done else gamma * V[ns_idx])
                if v > best_v:
                    best_v, best_a = v, a
                env.state = s
            if policy[s_idx] != best_a:
                policy[s_idx] = best_a
                stable = False
        if stable:
            break

    return V, policy, convergence

def value_iteration(env: GridWorld, gamma: float = 0.95, theta: float = 1e-6) -> Tuple[np.ndarray, np.ndarray, List[float]]:
    """Value Iteration: update V directly without policy evaluation loop."""
    n = env.n_states
    V = np.zeros(n)
    convergence = []

    while True:
        delta = 0
        for s_idx in range(n):
            s = env.idx_to_state(s_idx)
            if s in env.walls or env.is_terminal(s):
                continue
            values = []
            for a in range(4):
                env.state = s
                ns, r, done = env.step(a)
                ns_idx = env.state_to_idx(ns)
                values.append(r + (0 if done else gamma * V[ns_idx]))
                env.state = s
            new_v = max(values)
            delta = max(delta, abs(new_v - V[s_idx]))
            V[s_idx] = new_v
        convergence.append(delta)
        if delta < theta:
            break

    # Extract greedy policy
    policy = np.zeros(n, dtype=int)
    for s_idx in range(n):
        s = env.idx_to_state(s_idx)
        if s in env.walls or env.is_terminal(s):
            continue
        best_a, best_v = 0, -1e9
        for a in range(4):
            env.state = s
            ns, r, done = env.step(a)
            ns_idx = env.state_to_idx(ns)
            v = r + (0 if done else gamma * V[ns_idx])
            if v > best_v:
                best_v, best_a = v, a
            env.state = s
        policy[s_idx] = best_a

    return V, policy, convergence

# ── TD Learning ───────────────────────────────────────────────────────────────

def q_learning(env: GridWorld, episodes: int = 2000, alpha: float = 0.1,
               gamma: float = 0.95, epsilon: float = 1.0, epsilon_decay: float = 0.999) -> Tuple[np.ndarray, List[float]]:
    """Q-Learning (off-policy TD): Q(s,a) ← Q(s,a) + α[r + γ max Q(s',·) − Q(s,a)]"""
    Q = np.zeros((env.n_states, env.n_actions))
    rewards_per_ep = []

    for ep in range(episodes):
        s = env.reset()
        s_idx = env.state_to_idx(s)
        total_r = 0
        for _ in range(200):
            # ε-greedy
            if random.random() < epsilon:
                a = random.randint(0, 3)
            else:
                a = Q[s_idx].argmax()
            ns, r, done = env.step(a)
            ns_idx = env.state_to_idx(ns)
            # Q-Learning update (off-policy)
            Q[s_idx, a] += alpha * (r + gamma * (0 if done else Q[ns_idx].max()) - Q[s_idx, a])
            s_idx = ns_idx
            total_r += r
            if done:
                break
        rewards_per_ep.append(total_r)
        epsilon = max(0.01, epsilon * epsilon_decay)

    return Q, rewards_per_ep

def sarsa(env: GridWorld, episodes: int = 2000, alpha: float = 0.1,
          gamma: float = 0.95, epsilon: float = 1.0, epsilon_decay: float = 0.999) -> Tuple[np.ndarray, List[float]]:
    """SARSA (on-policy TD): Q(s,a) ← Q(s,a) + α[r + γ Q(s',a') − Q(s,a)]"""
    Q = np.zeros((env.n_states, env.n_actions))
    rewards_per_ep = []

    def eps_greedy(s_idx):
        if random.random() < epsilon:
            return random.randint(0, 3)
        return Q[s_idx].argmax()

    for ep in range(episodes):
        s = env.reset()
        s_idx = env.state_to_idx(s)
        a = eps_greedy(s_idx)
        total_r = 0
        for _ in range(200):
            ns, r, done = env.step(a)
            ns_idx = env.state_to_idx(ns)
            na = eps_greedy(ns_idx)
            # SARSA update (on-policy uses actual next action)
            Q[s_idx, a] += alpha * (r + gamma * (0 if done else Q[ns_idx, na]) - Q[s_idx, a])
            s_idx, a = ns_idx, na
            total_r += r
            if done:
                break
        rewards_per_ep.append(total_r)
        epsilon = max(0.01, epsilon * epsilon_decay)

    return Q, rewards_per_ep

# ── Visualization ─────────────────────────────────────────────────────────────

def visualize_policy(env: GridWorld, policy: np.ndarray, V: Optional[np.ndarray] = None, title: str = "Policy"):
    grid = [["·"] * env.size for _ in range(env.size)]
    for r in range(env.size):
        for c in range(env.size):
            s = (r, c)
            s_idx = env.state_to_idx(s)
            if s in env.walls:
                grid[r][c] = "X"
            elif env.is_terminal(s):
                grid[r][c] = "G"
            elif s == env.start:
                grid[r][c] = "S"
            else:
                grid[r][c] = env.ACTION_NAMES[policy[s_idx]]

    print(f"\n{title}")
    print("  " + " ".join(str(i) for i in range(env.size)))
    for i, row in enumerate(grid):
        print(f"{i} " + " ".join(row))

    if V is not None:
        print("\nValue Function:")
        print("  " + " ".join(f"{i:5d}" for i in range(env.size)))
        for r in range(env.size):
            row_vals = []
            for c in range(env.size):
                s_idx = env.state_to_idx((r, c))
                row_vals.append(f"{V[s_idx]:5.2f}")
            print(f"{r} " + " ".join(row_vals))

def plot_rewards(rewards_dict: Dict[str, List[float]]):
    try:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 5))
        for name, rewards in rewards_dict.items():
            window = 50
            if len(rewards) >= window:
                avg = [sum(rewards[i:i+window])/window for i in range(len(rewards)-window+1)]
                ax.plot(range(window-1, len(rewards)), avg, label=name)
        ax.set_title("GridWorld Learning Curves (Moving Average 50 ep)")
        ax.set_xlabel("Episode")
        ax.set_ylabel("Avg Total Reward")
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig("gridworld_learning.png", dpi=100)
        print("Plot saved to gridworld_learning.png")
        plt.show()
    except Exception as e:
        print(f"Plot skipped: {e}")

# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GridWorld RL")
    parser.add_argument("--algo", default="q_learning",
                        choices=["q_learning", "sarsa", "policy_iteration", "value_iteration"])
    parser.add_argument("--episodes", type=int, default=2000)
    parser.add_argument("--visualize", action="store_true")
    parser.add_argument("--compare", action="store_true")
    args = parser.parse_args()

    env = GridWorld(size=5)

    if args.compare:
        print("Comparing Q-Learning vs SARSA vs Value Iteration on GridWorld 5×5\n")
        Q_ql, r_ql = q_learning(env, episodes=args.episodes)
        Q_s, r_s = sarsa(env, episodes=args.episodes)
        _, policy_vi, _ = value_iteration(env)

        print(f"Q-Learning final avg reward (last 100): {sum(r_ql[-100:])/100:.2f}")
        print(f"SARSA     final avg reward (last 100): {sum(r_s[-100:])/100:.2f}")

        policy_ql = Q_ql.argmax(axis=1)
        policy_s = Q_s.argmax(axis=1)
        visualize_policy(env, policy_ql, title="Q-Learning Policy")
        visualize_policy(env, policy_s, title="SARSA Policy")
        visualize_policy(env, policy_vi, title="Value Iteration Policy")

        if args.visualize:
            plot_rewards({"Q-Learning": r_ql, "SARSA": r_s})

    elif args.algo == "q_learning":
        print(f"Q-Learning on GridWorld ({args.episodes} episodes)...")
        Q, rewards = q_learning(env, episodes=args.episodes)
        print(f"Final avg reward (last 100 eps): {sum(rewards[-100:])/100:.2f}")
        policy = Q.argmax(axis=1)
        visualize_policy(env, policy, title="Q-Learning Greedy Policy")
        if args.visualize:
            plot_rewards({"Q-Learning": rewards})

    elif args.algo == "sarsa":
        print(f"SARSA on GridWorld ({args.episodes} episodes)...")
        Q, rewards = sarsa(env, episodes=args.episodes)
        print(f"Final avg reward (last 100 eps): {sum(rewards[-100:])/100:.2f}")
        policy = Q.argmax(axis=1)
        visualize_policy(env, policy, title="SARSA Greedy Policy")
        if args.visualize:
            plot_rewards({"SARSA": rewards})

    elif args.algo == "policy_iteration":
        print("Policy Iteration...")
        V, policy, conv = policy_iteration(env)
        print(f"Converged in {len(conv)} evaluation steps")
        visualize_policy(env, policy, V, title="Policy Iteration")

    elif args.algo == "value_iteration":
        print("Value Iteration...")
        V, policy, conv = value_iteration(env)
        print(f"Converged in {len(conv)} sweeps (final Δ = {conv[-1]:.2e})")
        visualize_policy(env, policy, V, title="Value Iteration")
