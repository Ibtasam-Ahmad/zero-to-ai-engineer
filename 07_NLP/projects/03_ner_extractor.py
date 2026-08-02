"""
Named Entity Extractor spaCy + Hugging Face NER
Requirements: spacy transformers torch pandas
Also run: python -m spacy download en_core_web_sm
Usage:
  python 03_ner_extractor.py --text "Apple CEO Tim Cook visited London last Monday."
  python 03_ner_extractor.py --file article.txt --output results.csv
  python 03_ner_extractor.py --folder ./texts/ --output results.json
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

# ── Entity extraction ─────────────────────────────────────────────────────────

ENTITY_LABELS = {"PERSON", "ORG", "GPE", "DATE", "MONEY", "LOC", "PRODUCT", "EVENT"}

def extract_spacy(text: str) -> List[Dict]:
    """Extract entities using spaCy."""
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("spaCy model not found. Run: python -m spacy download en_core_web_sm")
        return []

    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ in ENTITY_LABELS:
            entities.append({
                "text": ent.text.strip(),
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char,
                "source": "spacy",
            })
    return entities

def extract_hf(text: str) -> List[Dict]:
    """Extract entities using Hugging Face NER pipeline."""
    try:
        from transformers import pipeline
        ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
    except Exception as e:
        print(f"HF NER unavailable: {e}")
        return []

    # HF NER label map to our standard labels
    label_map = {
        "PER": "PERSON", "ORG": "ORG", "LOC": "GPE", "MISC": "MISC",
    }
    results = ner(text[:512])
    entities = []
    for r in results:
        label = label_map.get(r["entity_group"], r["entity_group"])
        if label in ENTITY_LABELS or label == "MISC":
            entities.append({
                "text": r["word"].strip(),
                "label": label,
                "start": r["start"],
                "end": r["end"],
                "score": round(r["score"], 4),
                "source": "huggingface",
            })
    return entities

def deduplicate(entities: List[Dict]) -> List[Dict]:
    """Deduplicate by (text, label) pair, keeping highest score."""
    seen: Dict[Tuple, Dict] = {}
    for ent in entities:
        key = (ent["text"].lower(), ent["label"])
        if key not in seen:
            seen[key] = ent
    return list(seen.values())

def count_frequencies(entities: List[Dict]) -> Dict[str, Counter]:
    """Count entity frequencies by label."""
    freq: Dict[str, Counter] = defaultdict(Counter)
    for ent in entities:
        freq[ent["label"]][ent["text"]] += 1
    return dict(freq)

# ── Output ────────────────────────────────────────────────────────────────────

def print_entities(entities: List[Dict], freq: Dict[str, Counter]):
    print(f"\n{'='*60}")
    print(f"  Found {len(entities)} unique entities")
    print(f"{'='*60}")
    for label in sorted(freq.keys()):
        print(f"\n  [{label}]")
        for text, count in freq[label].most_common(10):
            print(f"    • {text} (×{count})")

def visualize_spacy(text: str):
    """Render NER visualization in terminal (or save HTML)."""
    try:
        import spacy
        from spacy import displacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text[:2000])
        # Save HTML
        html = displacy.render(doc, style="ent", page=True)
        out = Path("ner_visualization.html")
        out.write_text(html)
        print(f"\n  Visualization saved to: {out.resolve()}")
    except Exception as e:
        print(f"  Visualization skipped: {e}")

def save_results(entities: List[Dict], freq: Dict[str, Counter], output: str):
    out = Path(output)
    if out.suffix == ".csv":
        import csv
        with out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["text", "label", "source", "score"])
            writer.writeheader()
            for ent in entities:
                writer.writerow({
                    "text": ent["text"],
                    "label": ent["label"],
                    "source": ent.get("source", ""),
                    "score": ent.get("score", ""),
                })
        print(f"  Saved CSV to {out}")
    else:
        payload = {"entities": entities, "frequencies": {k: dict(v) for k, v in freq.items()}}
        out.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        print(f"  Saved JSON to {out}")

# ── Main ──────────────────────────────────────────────────────────────────────

def process_text(text: str, backend: str = "both") -> Tuple[List[Dict], Dict[str, Counter]]:
    entities = []
    if backend in ("spacy", "both"):
        entities += extract_spacy(text)
    if backend in ("hf", "both"):
        entities += extract_hf(text)
    deduped = deduplicate(entities)
    freq = count_frequencies(deduped)
    return deduped, freq

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Named Entity Extractor")
    parser.add_argument("--text", type=str, help="Text string to analyze")
    parser.add_argument("--file", type=str, help="Path to a text file")
    parser.add_argument("--folder", type=str, help="Folder of .txt files")
    parser.add_argument("--output", type=str, help="Output file (CSV or JSON)")
    parser.add_argument("--backend", choices=["spacy", "hf", "both"], default="spacy")
    parser.add_argument("--visualize", action="store_true", help="Save displacy HTML")
    args = parser.parse_args()

    # Collect input text(s)
    texts: Dict[str, str] = {}
    if args.text:
        texts["<inline>"] = args.text
    elif args.file:
        p = Path(args.file)
        texts[p.name] = p.read_text(encoding="utf-8")
    elif args.folder:
        folder = Path(args.folder)
        for p in folder.glob("*.txt"):
            texts[p.name] = p.read_text(encoding="utf-8")
    else:
        # Demo
        texts["demo"] = (
            "Elon Musk, CEO of Tesla and SpaceX, visited London on Monday to meet with UK Prime Minister. "
            "Microsoft acquired Activision Blizzard for $68.7 billion in January 2023. "
            "OpenAI, backed by Microsoft, released GPT-4 in San Francisco. "
            "Apple reported $90 billion revenue last quarter."
        )

    all_entities: List[Dict] = []
    for name, text in texts.items():
        print(f"\nProcessing: {name} ({len(text)} chars)")
        ents, freq = process_text(text, backend=args.backend)
        all_entities.extend(ents)
        print_entities(ents, freq)
        if args.visualize and len(texts) == 1:
            visualize_spacy(text)

    if args.output and all_entities:
        combined_freq = count_frequencies(all_entities)
        save_results(all_entities, combined_freq, args.output)
