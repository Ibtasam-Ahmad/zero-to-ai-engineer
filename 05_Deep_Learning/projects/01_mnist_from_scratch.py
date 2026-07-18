"""
MNIST Neural Network from Scratch (NumPy only)
Full MLP: forward pass, backprop, mini-batch SGD, ReLU, softmax, cross-entropy.
No PyTorch/TensorFlow. Target: >95% accuracy.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import time


# ─── Activation Functions ────────────────────────────────────────────────────

def relu(z):
    """ReLU activation: f(z) = max(0, z)"""
    return np.maximum(0, z)


def relu_derivative(z):
    """Derivative of ReLU: f'(z) = 1 if z > 0 else 0"""
    return (z > 0).astype(float)


def softmax(z):
    """Numerically stable softmax: exp(z - max) / sum(exp(z - max))"""
    z_stable = z - np.max(z, axis=1, keepdims=True)
    exp_z = np.exp(z_stable)
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)


# ─── Loss Function ────────────────────────────────────────────────────────────

def cross_entropy_loss(y_pred, y_true):
    """
    Cross-entropy loss:
        L = -1/m * sum(y_true * log(y_pred + eps))
    """
    m = y_true.shape[0]
    log_likelihood = -np.sum(y_true * np.log(y_pred + 1e-8))
    return log_likelihood / m


# ─── Weight Initialization ────────────────────────────────────────────────────

def he_init(fan_in, fan_out):
    """He initialization: W ~ N(0, sqrt(2/fan_in)) for ReLU layers"""
    return np.random.randn(fan_in, fan_out) * np.sqrt(2.0 / fan_in)


# ─── MLP Network ─────────────────────────────────────────────────────────────

class MLP:
    """
    Multi-Layer Perceptron with:
    - Architecture: 784 → 256 → 128 → 10
    - Activations: ReLU (hidden), Softmax (output)
    - Optimizer: Mini-batch SGD with momentum
    """

    def __init__(self, layer_sizes, lr=0.01, momentum=0.9):
        self.layer_sizes = layer_sizes
        self.lr = lr
        self.momentum = momentum
        self.params = {}
        self.velocities = {}

        # Initialize weights and biases
        for i in range(len(layer_sizes) - 1):
            n_in, n_out = layer_sizes[i], layer_sizes[i + 1]
            self.params[f"W{i+1}"] = he_init(n_in, n_out)
            self.params[f"b{i+1}"] = np.zeros((1, n_out))
            self.velocities[f"W{i+1}"] = np.zeros((n_in, n_out))
            self.velocities[f"b{i+1}"] = np.zeros((1, n_out))

    def forward(self, X):
        """
        Forward pass through all layers.
        Cache activations for backprop.
        """
        cache = {"A0": X}
        n_layers = len(self.layer_sizes) - 1

        for i in range(1, n_layers + 1):
            Z = cache[f"A{i-1}"] @ self.params[f"W{i}"] + self.params[f"b{i}"]
            cache[f"Z{i}"] = Z
            if i < n_layers:
                cache[f"A{i}"] = relu(Z)  # Hidden layers: ReLU
            else:
                cache[f"A{i}"] = softmax(Z)  # Output layer: Softmax

        return cache

    def backward(self, cache, y_true):
        """
        Backpropagation: compute gradients using chain rule.
        dL/dW = A^T · dL/dZ
        dL/dZ = dL/dA · activation'(Z)
        """
        grads = {}
        m = y_true.shape[0]
        n_layers = len(self.layer_sizes) - 1

        # Output layer gradient (softmax + cross-entropy combined)
        # dL/dZ_output = (y_pred - y_true) / m
        dZ = (cache[f"A{n_layers}"] - y_true) / m

        for i in range(n_layers, 0, -1):
            A_prev = cache[f"A{i-1}"]
            grads[f"dW{i}"] = A_prev.T @ dZ
            grads[f"db{i}"] = np.sum(dZ, axis=0, keepdims=True)

            if i > 1:
                # Backprop through ReLU
                dA = dZ @ self.params[f"W{i}"].T
                dZ = dA * relu_derivative(cache[f"Z{i-1}"])

        return grads

    def update(self, grads):
        """SGD with momentum: v = β·v + lr·grad, W = W - v"""
        for i in range(1, len(self.layer_sizes)):
            for p in ["W", "b"]:
                key = f"{p}{i}"
                # Momentum update
                self.velocities[key] = (self.momentum * self.velocities[key]
                                        + self.lr * grads[f"d{key}"])
                self.params[key] -= self.velocities[key]

    def predict(self, X):
        """Predict class labels."""
        cache = self.forward(X)
        return np.argmax(cache[f"A{len(self.layer_sizes)-1}"], axis=1)

    def accuracy(self, X, y_labels):
        """Compute accuracy."""
        preds = self.predict(X)
        return np.mean(preds == y_labels)


# ─── Training Loop ────────────────────────────────────────────────────────────

def train(model, X_train, y_train_oh, y_train_labels,
          X_val, y_val_labels, epochs=30, batch_size=64):
    """Mini-batch training loop."""
    m = X_train.shape[0]
    history = {"train_loss": [], "train_acc": [], "val_acc": []}

    for epoch in range(1, epochs + 1):
        t0 = time.time()
        # Shuffle training data
        indices = np.random.permutation(m)
        X_shuf = X_train[indices]
        y_shuf = y_train_oh[indices]
        epoch_loss = 0

        # Mini-batch updates
        for start in range(0, m, batch_size):
            X_batch = X_shuf[start:start + batch_size]
            y_batch = y_shuf[start:start + batch_size]

            cache = model.forward(X_batch)
            n_layers = len(model.layer_sizes) - 1
            loss = cross_entropy_loss(cache[f"A{n_layers}"], y_batch)
            grads = model.backward(cache, y_batch)
            model.update(grads)
            epoch_loss += loss

        avg_loss = epoch_loss / (m // batch_size)
        train_acc = model.accuracy(X_train, y_train_labels)
        val_acc = model.accuracy(X_val, y_val_labels)

        history["train_loss"].append(avg_loss)
        history["train_acc"].append(train_acc)
        history["val_acc"].append(val_acc)

        elapsed = time.time() - t0
        print(f"Epoch {epoch:3d}/{epochs} | Loss: {avg_loss:.4f} | "
              f"Train Acc: {train_acc:.4f} | Val Acc: {val_acc:.4f} | {elapsed:.1f}s")

    return history


def plot_history(history):
    """Plot training curves."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(history["train_loss"], label="Train Loss", color="#e74c3c")
    axes[0].set_title("Training Loss")
    axes[0].set_xlabel("Epoch")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(history["train_acc"], label="Train Acc", color="#2ecc71")
    axes[1].plot(history["val_acc"], label="Val Acc", color="#3498db")
    axes[1].set_title("Accuracy")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylim(0, 1)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("mnist_training.png", dpi=100)
    print("Training curves saved to mnist_training.png")
    plt.close()


def visualize_predictions(model, X_test, y_test):
    """Show 16 sample predictions."""
    indices = np.random.choice(len(X_test), 16, replace=False)
    X_sample = X_test[indices]
    y_pred = model.predict(X_sample)
    y_true = y_test[indices]

    fig, axes = plt.subplots(4, 4, figsize=(8, 8))
    for i, ax in enumerate(axes.flatten()):
        ax.imshow(X_sample[i].reshape(28, 28), cmap="gray")
        color = "green" if y_pred[i] == y_true[i] else "red"
        ax.set_title(f"P:{y_pred[i]} T:{y_true[i]}", color=color, fontsize=8)
        ax.axis("off")
    plt.suptitle("MNIST Predictions (Green=Correct, Red=Wrong)")
    plt.tight_layout()
    plt.savefig("mnist_predictions.png", dpi=100)
    print("Predictions saved to mnist_predictions.png")
    plt.close()


if __name__ == "__main__":
    print("=" * 55)
    print("  MNIST NEURAL NETWORK FROM SCRATCH (NumPy only)")
    print("=" * 55)

    # Load MNIST
    print("\n[1] Loading MNIST...")
    try:
        mnist = fetch_openml("mnist_784", version=1, as_frame=False, parser="auto")
        X, y = mnist.data, mnist.target.astype(int)
    except Exception:
        print("Generating random MNIST-like data for demo...")
        X = np.random.rand(10000, 784)
        y = np.random.randint(0, 10, 10000)

    X = X / 255.0  # Normalize to [0, 1]
    print(f"Data shape: X={X.shape}, y={y.shape}")

    # Train/val/test split
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
    print(f"Train: {len(X_train)} | Val: {len(X_val)} | Test: {len(X_test)}")

    # One-hot encode labels
    ohe = OneHotEncoder(sparse_output=False)
    y_train_oh = ohe.fit_transform(y_train.reshape(-1, 1))

    # Build model: 784 → 256 → 128 → 10
    print("\n[2] Building MLP: 784 → 256 → 128 → 10")
    model = MLP(layer_sizes=[784, 256, 128, 10], lr=0.01, momentum=0.9)

    # Train
    print("\n[3] Training...")
    history = train(model, X_train, y_train_oh, y_train, X_val, y_val,
                    epochs=20, batch_size=64)

    # Final evaluation
    test_acc = model.accuracy(X_test, y_test)
    print(f"\n[4] Final Test Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")

    if test_acc >= 0.95:
        print("✓ Achieved >95% accuracy!")
    else:
        print(f"Reached {test_acc*100:.1f}% try more epochs or tune LR.")

    # Plots
    print("\n[5] Plotting...")
    plot_history(history)
    visualize_predictions(model, X_test, y_test)

    print("\nDone! All built with NumPy only no deep learning frameworks.")
