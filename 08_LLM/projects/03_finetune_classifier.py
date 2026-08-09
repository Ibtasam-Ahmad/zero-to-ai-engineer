"""
Fine-tune Small LLM for Text Classification Unsloth + LoRA + Llama-3.2-1B
Requirements: unsloth transformers datasets trl peft torch accelerate huggingface_hub
Usage:
  python 03_finetune_classifier.py --train
  python 03_finetune_classifier.py --train --push-to-hub your-username/my-classifier
  python 03_finetune_classifier.py --infer --model ./finetuned-classifier --text "I love this product!"
"""

import argparse
import json
import os
from pathlib import Path
from typing import List

# ── Dataset preparation ───────────────────────────────────────────────────────

CATEGORIES = ["positive", "negative", "neutral"]

SAMPLE_DATA = [
    ("This product is absolutely amazing! Best purchase ever.", "positive"),
    ("Terrible quality, broke after one day. Total waste of money.", "negative"),
    ("It's okay. Does what it's supposed to do, nothing more.", "neutral"),
    ("I'm so happy with this purchase. Highly recommend!", "positive"),
    ("Awful experience. Customer service was unhelpful.", "negative"),
    ("The product arrived on time. Average quality.", "neutral"),
    ("Outstanding performance! Exceeded all my expectations.", "positive"),
    ("Do not buy this. Complete scam and poor build quality.", "negative"),
    ("Decent product for the price. Nothing special.", "neutral"),
    ("Fantastic! Will definitely buy again.", "positive"),
    ("Disappointed. The description was misleading.", "negative"),
    ("Works as described. Meets basic requirements.", "neutral"),
    ("Love it! Exactly what I needed. Five stars.", "positive"),
    ("Broke within a week. Very poor durability.", "negative"),
    ("It's fine. Not great, not terrible.", "neutral"),
    ("Incredible value for money! Superior quality.", "positive"),
    ("Worst product I've ever bought. Stay away.", "negative"),
    ("Satisfactory. Gets the job done.", "neutral"),
]

INSTRUCTION_TEMPLATE = """Below is a product review. Classify the sentiment as positive, negative, or neutral.

Review: {text}

Sentiment:"""

def prepare_dataset(data: List[tuple]) -> List[dict]:
    """Convert (text, label) pairs to instruction-following format."""
    samples = []
    for text, label in data:
        samples.append({
            "instruction": INSTRUCTION_TEMPLATE.format(text=text),
            "output": label,
            "full_text": INSTRUCTION_TEMPLATE.format(text=text) + " " + label,
        })
    return samples

def save_dataset(samples: List[dict], path: str = "./classification_dataset.json"):
    with open(path, "w") as f:
        json.dump(samples, f, indent=2)
    print(f"Dataset saved to {path} ({len(samples)} samples)")
    return path

# ── Training with Unsloth + LoRA ──────────────────────────────────────────────

def train(
    model_name: str = "unsloth/Llama-3.2-1B-Instruct",
    output_dir: str = "./finetuned-classifier",
    epochs: int = 3,
    push_to_hub: str = None,
):
    try:
        from unsloth import FastLanguageModel
    except ImportError:
        print("Unsloth not installed. Falling back to standard PEFT training.")
        train_standard(output_dir=output_dir, epochs=epochs, push_to_hub=push_to_hub)
        return

    from datasets import Dataset
    from trl import SFTTrainer, SFTConfig

    print(f"Loading model: {model_name}")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_name,
        max_seq_length=256,
        load_in_4bit=True,
    )

    # Apply LoRA
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_alpha=16,
        lora_dropout=0.05,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=42,
    )

    # Prepare dataset
    samples = prepare_dataset(SAMPLE_DATA)
    dataset = Dataset.from_list([{"text": s["full_text"]} for s in samples])

    training_args = SFTConfig(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=2,
        warmup_steps=10,
        learning_rate=2e-4,
        logging_steps=5,
        save_strategy="epoch",
        fp16=True,
        report_to="none",
        max_seq_length=256,
        dataset_text_field="text",
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer,
    )

    print("Starting training...")
    trainer.train()

    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Model saved to {output_dir}")

    if push_to_hub:
        print(f"Pushing to Hub: {push_to_hub}")
        model.push_to_hub(push_to_hub)
        tokenizer.push_to_hub(push_to_hub)
        print("Pushed to Hugging Face Hub!")

def train_standard(
    output_dir: str = "./finetuned-classifier",
    epochs: int = 3,
    push_to_hub: str = None,
):
    """Fallback training with standard transformers + PEFT (no Unsloth)."""
    from datasets import Dataset
    from peft import LoraConfig, get_peft_model, TaskType
    from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling

    model_name = "microsoft/phi-2"
    print(f"Loading fallback model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)

    lora_config = LoraConfig(
        r=8, lora_alpha=16, lora_dropout=0.1,
        target_modules=["q_proj", "v_proj"],
        task_type=TaskType.CAUSAL_LM,
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    samples = prepare_dataset(SAMPLE_DATA)

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=128)

    dataset = Dataset.from_list([{"text": s["full_text"]} for s in samples])
    tokenized = dataset.map(tokenize, batched=True, remove_columns=["text"])

    args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=2,
        logging_steps=5,
        save_strategy="epoch",
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )

    trainer.train()
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Model saved to {output_dir}")

# ── Inference ─────────────────────────────────────────────────────────────────

def infer(model_dir: str, text: str) -> str:
    from transformers import pipeline

    pipe = pipeline("text-generation", model=model_dir, max_new_tokens=10, device_map="auto")
    prompt = INSTRUCTION_TEMPLATE.format(text=text)
    result = pipe(prompt, temperature=0.1, do_sample=False)
    generated = result[0]["generated_text"]
    # Extract just the generated part
    if prompt in generated:
        answer = generated[len(prompt):].strip().split()[0].lower()
    else:
        answer = generated.strip().split()[-1].lower()

    # Normalize
    for cat in CATEGORIES:
        if cat in answer:
            return cat
    return answer

def evaluate(model_dir: str):
    """Evaluate on training data (demo purposes)."""
    print("\nEvaluating on sample data:")
    correct = 0
    for text, true_label in SAMPLE_DATA[:8]:
        pred = infer(model_dir, text)
        match = "✓" if pred == true_label else "✗"
        print(f"  {match} True: {true_label:<10} Pred: {pred:<10} | {text[:60]}")
        if pred == true_label:
            correct += 1
    print(f"\nAccuracy: {correct}/8 = {correct/8:.1%}")

# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fine-tune LLM Classifier")
    parser.add_argument("--train", action="store_true", help="Run training")
    parser.add_argument("--infer", action="store_true", help="Run inference")
    parser.add_argument("--evaluate", action="store_true", help="Evaluate model")
    parser.add_argument("--model", default="./finetuned-classifier", help="Model dir for inference")
    parser.add_argument("--text", type=str, help="Text to classify")
    parser.add_argument("--push-to-hub", type=str, help="HF Hub repo name to push model")
    parser.add_argument("--epochs", type=int, default=3)
    args = parser.parse_args()

    if args.train:
        samples = prepare_dataset(SAMPLE_DATA)
        save_dataset(samples)
        train(output_dir=args.model, epochs=args.epochs, push_to_hub=args.push_to_hub)
    elif args.infer and args.text:
        result = infer(args.model, args.text)
        print(f"\nText: {args.text}")
        print(f"Sentiment: {result}")
    elif args.evaluate:
        evaluate(args.model)
    else:
        parser.print_help()
        print("\nExample: python 03_finetune_classifier.py --train")
        print("         python 03_finetune_classifier.py --infer --text 'Great product!'")
