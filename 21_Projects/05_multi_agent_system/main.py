"""Entry point for the multi-agent research system."""

import sys
from graph import run_pipeline

if __name__ == "__main__":
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Large Language Models in 2024"
    print(f"\n🔍 Researching: {topic}\n{'='*60}")
    result = run_pipeline(topic)
    print("\n📋 Activity Log:")
    for entry in result.get("log", []):
        print(f"  {entry}")
    print("\n📄 Final Report:")
    print("="*60)
    print(result.get("final_report", "No report generated."))
