import sys
from pathlib import Path

# Configure UTF-8 stdout for Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config import DATA_RAW_DIR, RAW_TABLE_FILES, REPORTS_DIR, TABLES_DIR
from src.data_loader import (
    discover_csv_files,
    load_all_raw_tables,
    profile_dataframe,
    generate_data_dictionary_markdown
)
import pandas as pd


def main():
    print("=" * 70)
    print("INSIGHTLAB: Automated Data Ingestion & Profiling Engine")
    print("=" * 70)

    # 1. Discover files
    print("\n[Step 1] Discovering CSV files in raw directory...")
    catalog = discover_csv_files(DATA_RAW_DIR)
    for name, meta in catalog.items():
        print(f"  * {name:<45} : {meta['size_mb']:>6.2f} MB")

    # 2. Ingest all raw tables
    print("\n[Step 2] Ingesting all raw relational tables...")
    tables = load_all_raw_tables(DATA_RAW_DIR, RAW_TABLE_FILES)

    # 3. Profile each table
    print("\n[Step 3] Computing statistical and relational profiles...")
    profiles = []
    summary_rows = []

    for entity, df in tables.items():
        profile = profile_dataframe(df, table_name=entity)
        profiles.append(profile)

        # Log high level findings
        pks = [c["column_name"] for c in profile["columns"] if c["is_candidate_key"]]
        pk_str = ", ".join(pks) if pks else "None (Composite or FK)"
        print(f"  [OK] {entity:<20} | Rows: {profile['row_count']:>7,} | Cols: {profile['column_count']:>2} | PK: {pk_str}")

        summary_rows.append({
            "table_name": entity,
            "rows": profile["row_count"],
            "columns": profile["column_count"],
            "memory_mb": profile["memory_mb"],
            "duplicates": profile["duplicate_rows"],
            "candidate_keys": pk_str
        })

    # Save summary table
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(TABLES_DIR / "raw_tables_inventory.csv", index=False)
    print(f"\n[Info] Raw table inventory saved to {TABLES_DIR / 'raw_tables_inventory.csv'}")

    # 4. Generate & Save Markdown Data Dictionary
    print("\n[Step 4] Generating relational Markdown Data Dictionary...")
    dict_path = REPORTS_DIR / "data_dictionary.md"
    generate_data_dictionary_markdown(profiles, output_path=dict_path)
    print(f"  [OK] Data dictionary written to: {dict_path}")

    print("\n" + "=" * 70)
    print("Profiling Complete: All raw tables cataloged, profiled, and documented.")
    print("=" * 70)


if __name__ == "__main__":
    main()
