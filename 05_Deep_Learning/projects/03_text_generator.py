"""
Character-level Text Generator (RNN/LSTM)
Trains on a text corpus, samples new text using temperature scaling.
"""

import torch
import torch.nn as nn
import numpy as np
import os
import time
import math

# ─── Corpus ───────────────────────────────────────────────────────────────────

SAMPLE_TEXT = """
To be, or not to be, that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune,
Or to take arms against a sea of troubles,
And by opposing end them. To die—to sleep,
No more; and by a sleep to say we end
The heart-ache and the thousand natural shocks
That flesh is heir to: 'tis a consummation
Devoutly to be wish'd. To die, to sleep;
To sleep, perchance to dream—ay, there's the rub:
For in that sleep of death what dreams may come,
When we have shuffled off this mortal coil,
Must give us pause—there's the respect
That makes calamity of so long life.
For who would bear the whips and scorns of time,
Th'oppressor's wrong, the proud man's contumely,
The pangs of despis'd love, the law's delay,
The insolence of office, and the spurns
That patient merit of th'unworthy takes,
When he himself might his quietus make
With a bare bodkin? Who would fardels bear,
To grunt and sweat under a weary life,
But that the dread of something after death,
The undiscover'd country, from whose bourn
No traveller returns, puzzles the will,
And makes us rather bear those ills we have
Than fly to others that we know not of?
Thus conscience doth make cowards of us all,
And thus the native hue of resolution
Is sicklied o'er with the pale cast of thought,
And enterprises of great pitch and moment
With this regard their currents turn awry
And lose the name of action.
""" * 20  # Repeat to get more training data


# ─── Tokenizer ────────────────────────────────────────────────────────────────

class CharTokenizer:
    """Maps characters to integer indices and back."""

    def __init__(self, text):
        self.chars = sorted(set(text))
        self.vocab_size = len(self.chars)
        self.char2idx = {c: i for i, c in enumerate(self.chars)}
        self.idx2char = {i: c for c, i in self.char2idx.items()}

    def encode(self, text):
        return [self.char2idx[c] for c in text if c in self.char2idx]

    def decode(self, indices):
        return "".join(self.idx2char.get(i, "?") for i in indices)


# ─── Model ────────────────────────────────────────────────────────────────────

class CharLSTM(nn.Module):
    """
    Character-level LSTM language model.
    Architecture: Embedding → LSTM → Dropout → Linear
    """

    def __init__(self, vocab_size, embed_dim=64, hidden_size=256, num_layers=2, dropout=0.3):
        super().__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_size, num_layers=num_layers,
                            batch_first=True, dropout=dropout if num_layers > 1 else 0)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, hidden=None):
        emb = self.embed(x)
        out, hidden = self.lstm(emb, hidden)
        out = self.dropout(out)
        logits = self.fc(out)
        return logits, hidden

    def init_hidden(self, batch_size, device):
        """Initialize hidden state to zeros."""
        h = torch.zeros(self.num_layers, batch_size, self.hidden_size, device=device)
        c = torch.zeros(self.num_layers, batch_size, self.hidden_size, device=device)
        return (h, c)


# ─── Data Preparation ─────────────────────────────────────────────────────────

def prepare_batches(encoded, seq_len=100, batch_size=64):
    """Split encoded text into (input, target) batch pairs."""
    # Trim to fit exactly
    n_batches = (len(encoded) - 1) // (seq_len * batch_size)
    total = n_batches * seq_len * batch_size
    x = torch.LongTensor(encoded[:total]).reshape(batch_size, -1)
    y = torch.LongTensor(encoded[1:total+1]).reshape(batch_size, -1)

    # Yield sequence chunks
    for start in range(0, x.size(1), seq_len):
        yield x[:, start:start+seq_len], y[:, start:start+seq_len]


# ─── Temperature Sampling ─────────────────────────────────────────────────────

def sample_with_temperature(logits, temperature=1.0, top_k=0):
    """
    Sample next token from logits with temperature.
    temperature → 0: greedy (most likely token)
    temperature → ∞: uniform random
    """
    logits = logits / max(temperature, 1e-8)

    # Top-k filtering
    if top_k > 0:
        values, _ = torch.topk(logits, top_k)
        min_val = values[:, -1].unsqueeze(-1)
        logits[logits < min_val] = float("-inf")

    probs = torch.softmax(logits, dim=-1)
    return torch.multinomial(probs, num_samples=1)


def generate_text(model, tokenizer, seed_text, length=200, temperature=0.8, top_k=40, device="cpu"):
    """Generate text by sampling character by character."""
    model.eval()
    encoded = tokenizer.encode(seed_text)
    if not encoded:
        encoded = [0]

    x = torch.LongTensor(encoded).unsqueeze(0).to(device)
    hidden = model.init_hidden(1, device)
    generated = list(encoded)

    with torch.no_grad():
        # Process seed
        _, hidden = model(x, hidden)

        # Generate new characters
        x = torch.LongTensor([[generated[-1]]]).to(device)
        for _ in range(length):
            logits, hidden = model(x, hidden)
            next_token = sample_with_temperature(logits[0, -1:], temperature, top_k)
            char_idx = next_token.item()
            generated.append(char_idx)
            x = torch.LongTensor([[char_idx]]).to(device)

    return tokenizer.decode(generated)


# ─── Training ─────────────────────────────────────────────────────────────────

def train(model, encoded, tokenizer, epochs=20, seq_len=100, batch_size=32, lr=0.002, device="cpu"):
    model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)
    criterion = nn.CrossEntropyLoss()
    history = []

    for epoch in range(1, epochs + 1):
        model.train()
        t0 = time.time()
        total_loss = 0
        n_batches = 0

        hidden = model.init_hidden(batch_size, device)

        for x_batch, y_batch in prepare_batches(encoded, seq_len, batch_size):
            x_batch = x_batch.to(device)
            y_batch = y_batch.to(device)

            # Detach hidden state to prevent backprop through full history
            hidden = tuple(h.detach() for h in hidden)

            optimizer.zero_grad()
            logits, hidden = model(x_batch, hidden)
            loss = criterion(logits.reshape(-1, tokenizer.vocab_size), y_batch.reshape(-1))
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            total_loss += loss.item()
            n_batches += 1

        scheduler.step()
        avg_loss = total_loss / max(n_batches, 1)
        perplexity = math.exp(avg_loss)
        elapsed = time.time() - t0
        history.append({"epoch": epoch, "loss": avg_loss, "ppl": perplexity})
        print(f"Epoch {epoch:3d}/{epochs} | Loss: {avg_loss:.4f} | "
              f"PPL: {perplexity:.2f} | {elapsed:.1f}s")

    return history


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  CHARACTER-LEVEL TEXT GENERATOR (LSTM)")
    print("=" * 55)

    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {DEVICE}")

    # Load corpus
    print("\n[1] Preparing corpus...")
    text = SAMPLE_TEXT
    print(f"Corpus length: {len(text):,} characters")

    tokenizer = CharTokenizer(text)
    print(f"Vocabulary size: {tokenizer.vocab_size} unique characters")
    encoded = tokenizer.encode(text)

    # Build model
    print("\n[2] Building CharLSTM model...")
    model = CharLSTM(
        vocab_size=tokenizer.vocab_size,
        embed_dim=64,
        hidden_size=256,
        num_layers=2,
        dropout=0.3
    )
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Parameters: {total_params:,}")

    # Train
    print("\n[3] Training...")
    history = train(model, encoded, tokenizer, epochs=20, seq_len=100,
                    batch_size=32, lr=0.002, device=DEVICE)

    # Generate text with different temperatures
    print("\n[4] Generating text samples...")
    seed = "To be, or not to be"

    for temp in [0.5, 0.8, 1.2]:
        print(f"\n--- Temperature = {temp} ---")
        generated = generate_text(model, tokenizer, seed, length=150,
                                  temperature=temp, top_k=40, device=DEVICE)
        print(generated)

    # Training summary
    final = history[-1]
    print(f"\n=== Training Summary ===")
    print(f"Final Loss: {final['loss']:.4f}")
    print(f"Final Perplexity: {final['ppl']:.2f}")
    print("\nLower perplexity = better predictions.")
    print("\nDone!")
