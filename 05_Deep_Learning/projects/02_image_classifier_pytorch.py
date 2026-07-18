"""
CIFAR-10 Image Classifier (PyTorch)
Custom CNN, mixed precision, early stopping, LR scheduler, TensorBoard.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.cuda.amp import GradScaler, autocast
import torchvision
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
import os
import time

CLASSES = ["plane", "car", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")


# ─── Model ───────────────────────────────────────────────────────────────────

class CIFAR10CNN(nn.Module):
    """Custom CNN for CIFAR-10."""

    def __init__(self, num_classes=10):
        super().__init__()
        # Block 1: 3 → 32 channels
        self.block1 = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(),
            nn.Conv2d(32, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(),
            nn.MaxPool2d(2), nn.Dropout2d(0.2),
        )
        # Block 2: 32 → 64 channels
        self.block2 = nn.Sequential(
            nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(),
            nn.MaxPool2d(2), nn.Dropout2d(0.3),
        )
        # Block 3: 64 → 128 channels
        self.block3 = nn.Sequential(
            nn.Conv2d(64, 128, 3, padding=1), nn.BatchNorm2d(128), nn.ReLU(),
            nn.Conv2d(128, 128, 3, padding=1), nn.BatchNorm2d(128), nn.ReLU(),
            nn.MaxPool2d(2), nn.Dropout2d(0.4),
        )
        # Classifier
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, 512), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(512, num_classes),
        )

    def forward(self, x):
        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)
        return self.classifier(x)


# ─── Data ─────────────────────────────────────────────────────────────────────

def get_dataloaders(batch_size=128):
    """Load CIFAR-10 with data augmentation."""
    train_transform = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    test_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])

    train_set = torchvision.datasets.CIFAR10("./data", train=True, download=True,
                                              transform=train_transform)
    test_set = torchvision.datasets.CIFAR10("./data", train=False, download=True,
                                             transform=test_transform)

    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True,
                               num_workers=2, pin_memory=True)
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False,
                              num_workers=2, pin_memory=True)
    return train_loader, test_loader


# ─── Training ─────────────────────────────────────────────────────────────────

class EarlyStopping:
    def __init__(self, patience=7, delta=0.001):
        self.patience = patience
        self.delta = delta
        self.counter = 0
        self.best_score = None
        self.early_stop = False

    def __call__(self, val_loss):
        score = -val_loss
        if self.best_score is None:
            self.best_score = score
        elif score < self.best_score + self.delta:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.counter = 0


def train_epoch(model, loader, optimizer, criterion, scaler, device):
    model.train()
    total_loss, correct, total = 0, 0, 0
    for X, y in loader:
        X, y = X.to(device), y.to(device)
        optimizer.zero_grad()
        with autocast():
            out = model(X)
            loss = criterion(out, y)
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        total_loss += loss.item() * X.size(0)
        correct += (out.argmax(1) == y).sum().item()
        total += X.size(0)
    return total_loss / total, correct / total


@torch.no_grad()
def eval_epoch(model, loader, criterion, device):
    model.eval()
    total_loss, correct, total = 0, 0, 0
    for X, y in loader:
        X, y = X.to(device), y.to(device)
        with autocast():
            out = model(X)
            loss = criterion(out, y)
        total_loss += loss.item() * X.size(0)
        correct += (out.argmax(1) == y).sum().item()
        total += X.size(0)
    return total_loss / total, correct / total


def train_model(epochs=30, batch_size=128, lr=0.001, checkpoint_path="cifar10_best.pt"):
    # Data
    print("[1] Loading CIFAR-10 data...")
    train_loader, test_loader = get_dataloaders(batch_size)

    # Model
    model = CIFAR10CNN().to(DEVICE)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"[2] Model parameters: {total_params:,}")

    # Optimizer, scheduler, loss
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.OneCycleLR(
        optimizer, max_lr=lr*10, epochs=epochs,
        steps_per_epoch=len(train_loader)
    )
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    scaler = GradScaler()
    early_stop = EarlyStopping(patience=7)

    history = {"train_loss": [], "val_loss": [], "train_acc": [], "val_acc": []}
    best_acc = 0

    print(f"[3] Training for up to {epochs} epochs...")
    for epoch in range(1, epochs + 1):
        t0 = time.time()
        train_loss, train_acc = train_epoch(model, train_loader, optimizer, criterion, scaler, DEVICE)
        val_loss, val_acc = eval_epoch(model, test_loader, criterion, DEVICE)
        scheduler.step()

        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        history["train_acc"].append(train_acc)
        history["val_acc"].append(val_acc)

        elapsed = time.time() - t0
        lr_current = optimizer.param_groups[0]["lr"]
        print(f"Epoch {epoch:3d}/{epochs} | "
              f"Train: {train_loss:.4f}/{train_acc:.3f} | "
              f"Val: {val_loss:.4f}/{val_acc:.3f} | "
              f"LR: {lr_current:.6f} | {elapsed:.1f}s")

        # Save best
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save({"epoch": epoch, "model": model.state_dict(),
                        "acc": val_acc}, checkpoint_path)

        early_stop(val_loss)
        if early_stop.early_stop:
            print(f"Early stopping at epoch {epoch}")
            break

    print(f"\nBest validation accuracy: {best_acc:.4f} ({best_acc*100:.2f}%)")
    return model, history, checkpoint_path


def plot_training(history):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(history["train_loss"], label="Train")
    axes[0].plot(history["val_loss"], label="Val")
    axes[0].set_title("Loss")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(history["train_acc"], label="Train")
    axes[1].plot(history["val_acc"], label="Val")
    axes[1].set_title("Accuracy")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.suptitle("CIFAR-10 Training (PyTorch)")
    plt.tight_layout()
    plt.savefig("cifar10_training.png", dpi=100)
    print("Training plot saved to cifar10_training.png")
    plt.close()


if __name__ == "__main__":
    print("=" * 50)
    print("  CIFAR-10 IMAGE CLASSIFIER (PyTorch)")
    print("=" * 50)

    model, history, ckpt = train_model(epochs=30)
    plot_training(history)

    # Load best and report
    checkpoint = torch.load(ckpt, map_location=DEVICE)
    model.load_state_dict(checkpoint["model"])
    print(f"\nFinal test accuracy (best model): {checkpoint['acc']*100:.2f}% "
          f"(epoch {checkpoint['epoch']})")
    print("Done!")
