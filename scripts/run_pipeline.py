"""
run_pipeline.py

Master script for the Bluestock MF Capstone ETL pipeline.
Runs every stage of the pipeline in order:

1. data_ingestion   - load and inspect the 10 raw CSVs
2. live_nav_fetch   - fetch live NAV data from mfapi.in
3. fund_master_exploration - explore fund master, validate AMFI codes
4. clean_data       - clean nav_history, investor_transactions, scheme_performance
5. load_to_sqlite   - build bluestock_mf.db from the cleaned data

Run from the project root:
    python scripts/run_pipeline.py
"""

import subprocess
import sys
import os

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

PIPELINE_STEPS = [
    "data_ingestion.py",
    "live_nav_fetch.py",
    "fund_master_exploration.py",
    "clean_data.py",
    "load_to_sqlite.py",
]


def run_step(script_name: str) -> bool:
    """Run a single pipeline script and return True if it succeeded."""
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    print(f"\n{'=' * 60}")
    print(f"Running: {script_name}")
    print("=" * 60)

    result = subprocess.run([sys.executable, script_path])
    return result.returncode == 0


def main():
    print("Starting Bluestock MF ETL pipeline...\n")

    for step in PIPELINE_STEPS:
        success = run_step(step)
        if not success:
            print(f"\nPipeline stopped: {step} failed.")
            sys.exit(1)

    print("\nPipeline complete. All steps ran successfully.")
    print("Database ready at bluestock_mf.db")


if __name__ == "__main__":
    main()
