"""Standalone ingestion script: python ingest.py --docs-dir ./docs"""

import argparse
import main as rag

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-dir", default="./docs")
    args = parser.parse_args()
    n = rag.ingest_documents(args.docs_dir)
    print(f"Ingestion complete: {n} chunks stored in ChromaDB.")
