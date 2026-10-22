"""Standalone ingestion script: python ingest.py --docs-dir ./docs"""

import argparse
import main as rag

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-dir", default="./docs")
    parser.add_argument("--reset", action="store_true", help="delete all stored chunks first (e.g. after removing PDFs)")
    args = parser.parse_args()
    if args.reset:
        rag.reset_collection()
    n = rag.ingest_documents(args.docs_dir)
    print(f"Ingestion complete: {n} chunks stored in ChromaDB.")
