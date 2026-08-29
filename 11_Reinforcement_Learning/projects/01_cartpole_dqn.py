"""
DQN Agent for CartPole-v1 Double DQN + Experience Replay + Target Network
Requirements: gymnasium torch numpy matplotlib
Usage:
  python 01_cartpole_dqn.py --train --episodes 500
  python 01_cartpole_dqn.py --train --episodes 500 --render
  python 01_cartpole_dqn.py --test --model cartpole_dqn.pth
"""

import argparse
import random
from collections import deque
from typing import List, Tuple

import numpy as np

# ── Network ───────────────────────────────────────────────────────────────────

def build_network(state_dim: int, action_dim: int, hidden: int = 128):
    import torch.nn as nn
    return nn.Sequential(
        nn.Linear(state_dim, hidden),
        nn.ReLU(),
        nn.Linear(hidden, hidden),
        nn.ReLU(),
        nn.Linear(hidden, action_dim),
    )

# ── Replay Buffer ─────────────────────────────────────────────────────────────

class ReplayBuffer:
    def __init__(self, capacity: int = 10_000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)

# ── DQN Agent ─────────────────────────────────────────────────────────────────

class DQNAgent:
    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        lr: float = 1e-3,
        gamma: float = 0.99,
        epsilon: float = 1.0,
        epsilon_min: float = 0.01,
        epsilon_decay: float = 0.995,
        batch_size: int = 64,
        target_update: int = 10,
    ):
        import torch
        import torch.optim as optim

        self.action_dim = action_dim
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.target_update = target_update
        self.update_count = 0
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Online network (trained every step)
        self.online_net = build_network(state_dim, action_dim).to(self.device)
        # Target network (updated periodically) Double DQN trick
        self.target_net = build_network(state_dim, action_dim).to(self.device)
        self.target_net.load_state_dict(self.online_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.Adam(self.online_net.parameters(), lr=lr)
        self.loss_fn = torch.nn.MSELoss()
        self.memory = ReplayBuffer()

    def act(self, state: np.ndarray) -> int:
        """Epsilon-greedy action selection."""
        if random.random() < self.epsilon:
            return random.randint(0, self.action_dim - 1)
        import torch
        state_t = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.online_net(state_t)
        return q_values.argmax().item()

    def remember(self, state, action, reward, next_state, done):
        self.memory.push(state, action, reward, next_state, done)

    def train_step(self) -> float:
        """Sample a minibatch and perform one gradient update."""
        if len(self.memory) < self.batch_size:
            return 0.0
        import torch

        batch = self.memory.sample(self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states_t     = torch.FloatTensor(np.array(states)).to(self.device)
        actions_t    = torch.LongTensor(actions).unsqueeze(1).to(self.device)
        rewards_t    = torch.FloatTensor(rewards).unsqueeze(1).to(self.device)
        next_states_t = torch.FloatTensor(np.array(next_states)).to(self.device)
        dones_t      = torch.FloatTensor(dones).unsqueeze(1).to(self.device)

        # Current Q(s, a)
        current_q = self.online_net(states_t).gather(1, actions_t)

        # Double DQN: action selection with online net, evaluation with target net
        with torch.no_grad():
            next_actions = self.online_net(next_states_t).argmax(1, keepdim=True)
            next_q = self.target_net(next_states_t).gather(1, next_actions)
            target_q = rewards_t + self.gamma * next_q * (1 - dones_t)

        loss = self.loss_fn(current_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        # Gradient clipping for stability
        torch.nn.utils.clip_grad_norm_(self.online_net.parameters(), 1.0)
        self.optimizer.step()

        self.update_count += 1
        if self.update_count % self.target_update == 0:
            self.target_net.load_state_dict(self.online_net.state_dict())

        # Decay epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        return loss.item()

    def save(self, path: str):
        import torch
        torch.save({"online_net": self.online_net.state_dict(), "epsilon": self.epsilon}, path)
        print(f"Model saved to {path}")

    def load(self, path: str):
        import torch
        data = torch.load(path, map_location=self.device)
        self.online_net.load_state_dict(data["online_net"])
        self.target_net.load_state_dict(data["online_net"])
        self.epsilon = data.get("epsilon", self.epsilon_min)

# ── Training loop ─────────────────────────────────────────────────────────────

def train(episodes: int = 500, render: bool = False, save_path: str = "cartpole_dqn.pth"):
    import gymnasium as gym

    env = gym.make("CartPole-v1", render_mode="human" if render else None)
    state_dim = env.observation_space.shape[0]   # 4
    action_dim = env.action_space.n               # 2

    agent = DQNAgent(state_dim, action_dim)
    rewards_history: List[float] = []
    losses_history: List[float] = []
    solved_at = None

    print(f"Training DQN on CartPole-v1 | state_dim={state_dim}, action_dim={action_dim}")
    print(f"Device: {'cuda' if agent.device.type == 'cuda' else 'cpu'}\n")

    for ep in range(1, episodes + 1):
        state, _ = env.reset()
        total_reward = 0
        ep_losses = []

        while True:
            action = agent.act(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            agent.remember(state, action, reward, next_state, float(done))
            loss = agent.train_step()
            if loss > 0:
                ep_losses.append(loss)
            state = next_state
            total_reward += reward
            if done:
                break

        rewards_history.append(total_reward)
        avg_loss = sum(ep_losses) / len(ep_losses) if ep_losses else 0
        losses_history.append(avg_loss)
        avg_reward_100 = sum(rewards_history[-100:]) / min(len(rewards_history), 100)

        if ep % 50 == 0:
            print(f"Ep {ep:>4}/{episodes} | Reward: {total_reward:>6.1f} | "
                  f"Avg(100): {avg_reward_100:>6.1f} | ε: {agent.epsilon:.3f} | Loss: {avg_loss:.4f}")

        if avg_reward_100 >= 475 and solved_at is None:
            solved_at = ep
            print(f"\n🎉 Solved at episode {ep}! Avg reward (last 100): {avg_reward_100:.1f}")
            agent.save(save_path)

    env.close()
    if solved_at is None:
        agent.save(save_path)

    _plot_training(rewards_history, losses_history, solved_at)
    return rewards_history

def _plot_training(rewards: List[float], losses: List[float], solved_at: int):
    try:
        import matplotlib.pyplot as plt
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        ax1.plot(rewards, alpha=0.4, label="Episode reward")
        window = 50
        if len(rewards) >= window:
            avg = [sum(rewards[i:i+window])/window for i in range(len(rewards)-window+1)]
            ax1.plot(range(window-1, len(rewards)), avg, label=f"Moving avg ({window})")
        if solved_at:
            ax1.axvline(solved_at, color="green", linestyle="--", label=f"Solved ep {solved_at}")
        ax1.set_title("CartPole DQN Training Episode Rewards")
        ax1.set_ylabel("Total Reward")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        ax2.plot(losses, alpha=0.6)
        ax2.set_title("Training Loss")
        ax2.set_xlabel("Episode")
        ax2.set_ylabel("MSE Loss")
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig("cartpole_training.png", dpi=100)
        print("Training plot saved to cartpole_training.png")
        plt.show()
    except Exception as e:
        print(f"Plot skipped: {e}")

# ── Testing ───────────────────────────────────────────────────────────────────

def test(model_path: str, episodes: int = 10):
    import gymnasium as gym
    env = gym.make("CartPole-v1", render_mode="human")
    state_dim, action_dim = env.observation_space.shape[0], env.action_space.n
    agent = DQNAgent(state_dim, action_dim)
    agent.load(model_path)
    agent.epsilon = 0  # Pure exploitation

    print(f"Testing {model_path} for {episodes} episodes...")
    total_rewards = []
    for ep in range(1, episodes + 1):
        state, _ = env.reset()
        total = 0
        while True:
            action = agent.act(state)
            state, reward, terminated, truncated, _ = env.step(action)
            total += reward
            if terminated or truncated:
                break
        total_rewards.append(total)
        print(f"  Episode {ep}: {total:.0f}")

    env.close()
    print(f"\nAvg reward: {sum(total_rewards)/len(total_rewards):.1f}")

# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DQN CartPole Agent")
    parser.add_argument("--train", action="store_true")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--episodes", type=int, default=500)
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--model", default="cartpole_dqn.pth")
    args = parser.parse_args()

    if args.train:
        train(episodes=args.episodes, render=args.render, save_path=args.model)
    elif args.test:
        test(args.model, episodes=5)
    else:
        print("CartPole DQN Agent")
        print("  --train            Train the agent")
        print("  --train --render   Train with visualization")
        print("  --test --model X   Test a saved model")
        print("  --episodes N       Number of training episodes (default 500)")
