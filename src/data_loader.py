"""Data Ingestion, Safe Loading, and Profiling Engine for InsightLab.

Provides reusable utilities for discovering, safely loading, profiling,
and generating comprehensive data dictionaries for multi-table CSV datasets.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import logging
import pandas as pd
import numpy as np

# Configure module-level logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def discover_csv_files(directory: Path) -> Dict[str, Dict[str, Any]]:
    """Scan a directory and catalog all CSV files with metadata.

    Args:
        directory: Directory path to scan.

    Returns:
        Dictionary mapping filename to file metadata (size, path, modified).
    """
    directory = Path(directory)
    if not directory.exists() or not directory.is_dir():
        logger.error(f"Target directory does not exist: {directory}")
        return {}

    catalog = {}
    for file_path in sorted(directory.glob("*.csv")):
        stat = file_path.stat()
        catalog[file_path.name] = {
            "path": file_path,
            "size_bytes": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 3),
            "modified_time": stat.st_mtime
        }
    logger.info(f"Discovered {len(catalog)} CSV files in {directory}")
    return catalog


def load_csv_safely(
    file_path: Union[str, Path],
    nrows: Optional[int] = None,
    parse_dates: Optional[List[str]] = None,
    dtype: Optional[Dict[str, Any]] = None,
    low_memory: bool = False
) -> pd.DataFrame:
    """Safely load a CSV file into a Pandas DataFrame with error handling.

    Args:
        file_path: Path to the CSV file.
        nrows: Optional maximum rows to load (useful for previews/profiling).
        parse_dates: Optional list of columns to parse as datetime.
        dtype: Optional dictionary of column data types.
        low_memory: Internally process the file in chunks to reduce memory.

    Returns:
        Pandas DataFrame of the loaded data.
    """
    path = Path(file_path)
    if not path.exists():
        logger.error(f"File not found: {path}")
        raise FileNotFoundError(f"File not found: {path}")

    try:
        df = pd.read_csv(
            path,
            nrows=nrows,
            parse_dates=parse_dates,
            dtype=dtype,
            low_memory=low_memory,
            encoding="utf-8"
        )
        mem_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
        logger.info(f"Loaded '{path.name}': {len(df):,} rows, {len(df.columns)} cols ({mem_mb:.2f} MB)")
        return df
    except UnicodeDecodeError:
        logger.warning(f"UTF-8 decode failed for {path.name}; falling back to 'latin-1' encoding.")
        df = pd.read_csv(path, nrows=nrows, parse_dates=parse_dates, dtype=dtype, encoding="latin-1")
        return df
    except Exception as e:
        logger.error(f"Critical error loading {path.name}: {e}")
        raise


def load_all_raw_tables(
    data_dir: Path,
    file_mapping: Dict[str, str],
    nrows: Optional[int] = None
) -> Dict[str, pd.DataFrame]:
    """Load all configured raw tables into an in-memory dictionary.

    Args:
        data_dir: Path to raw directory.
        file_mapping: Dict mapping logical entity names to filenames.
        nrows: Optional row limit for fast profiling.

    Returns:
        Dictionary mapping logical name (e.g. 'orders') to DataFrame.
    """
    data_dir = Path(data_dir)
    tables = {}
    for entity_name, filename in file_mapping.items():
        file_path = data_dir / filename
        if file_path.exists():
            tables[entity_name] = load_csv_safely(file_path, nrows=nrows)
        else:
            logger.warning(f"File '{filename}' for entity '{entity_name}' does not exist in {data_dir}.")
    return tables


def profile_dataframe(df: pd.DataFrame, table_name: str = "dataset") -> Dict[str, Any]:
    """Perform a comprehensive statistical and data quality profile of a DataFrame.

    Computes:
    - Shape, total memory footprint, and exact duplicate row counts.
    - Column data types, null counts, null percentages.
    - Uniqueness cardinality and candidate primary key detection.
    - Summary distribution statistics (min, mean, max, std, skew) for numerics.
    - High-frequency values for categoricals.

    Args:
        df: Input DataFrame.
        table_name: Identifier name for reporting.

    Returns:
        Structured dictionary containing the profile metrics.
    """
    total_rows = len(df)
    total_cols = len(df.columns)
    mem_usage_mb = round(df.memory_usage(deep=True).sum() / (1024 * 1024), 3)
    duplicate_rows = int(df.duplicated().sum())

    col_profiles = []
    for col in df.columns:
        series = df[col]
        null_count = int(series.isna().sum())
        null_pct = round((null_count / total_rows) * 100, 2) if total_rows > 0 else 0.0
        n_unique = int(series.nunique(dropna=True))
        unique_pct = round((n_unique / total_rows) * 100, 2) if total_rows > 0 else 0.0

        # Candidate primary key test: zero nulls and 100% unique values
        is_candidate_key = (null_count == 0) and (n_unique == total_rows) and (total_rows > 0)

        # Sample values for inspection
        sample_vals = series.dropna().unique()[:3].tolist()
        sample_str = ", ".join([str(val) for val in sample_vals])

        col_meta = {
            "column_name": col,
            "data_type": str(series.dtype),
            "non_null_count": total_rows - null_count,
            "null_count": null_count,
            "null_pct": null_pct,
            "unique_count": n_unique,
            "unique_pct": unique_pct,
            "is_candidate_key": is_candidate_key,
            "sample_values": sample_str
        }

        # Numerical statistics
        if pd.api.types.is_numeric_dtype(series):
            valid_num = series.dropna()
            if len(valid_num) > 0:
                col_meta["min"] = round(float(valid_num.min()), 2)
                col_meta["mean"] = round(float(valid_num.mean()), 2)
                col_meta["median"] = round(float(valid_num.median()), 2)
                col_meta["max"] = round(float(valid_num.max()), 2)
                col_meta["std"] = round(float(valid_num.std()), 2)
                col_meta["skew"] = round(float(valid_num.skew()), 2)
        elif pd.api.types.is_object_dtype(series) or pd.api.types.is_categorical_dtype(series):
            mode_series = series.mode()
            if not mode_series.empty:
                col_meta["top_value"] = str(mode_series.iloc[0])
                col_meta["top_freq"] = int((series == mode_series.iloc[0]).sum())

        col_profiles.append(col_meta)

    return {
        "table_name": table_name,
        "row_count": total_rows,
        "column_count": total_cols,
        "memory_mb": mem_usage_mb,
        "duplicate_rows": duplicate_rows,
        "duplicate_pct": round((duplicate_rows / total_rows) * 100, 2) if total_rows > 0 else 0.0,
        "columns": col_profiles
    }


def generate_data_dictionary_markdown(
    profiles: List[Dict[str, Any]],
    output_path: Optional[Path] = None
) -> str:
    """Generate a GitHub-flavored Markdown data dictionary from profiles.

    Args:
        profiles: List of table profile dictionaries.
        output_path: Optional destination file path to save the markdown.

    Returns:
        Formatted markdown string.
    """
    md_lines = [
        "# InsightLab — Relational Data Dictionary & Schema Profile",
        "",
        "> **Platform**: InsightLab Advanced Analytics Engine  ",
        "> **Source Dataset**: Olist E-Commerce Brazilian Relational Database  ",
        "> **Status**: Raw Baseline Inspection  ",
        "",
        "## Summary of Ingested Tables",
        "",
        "| Table Name | Total Rows | Total Columns | Memory (MB) | Duplicate Rows |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]

    for p in profiles:
        md_lines.append(
            f"| **`{p['table_name']}`** | {p['row_count']:,} | {p['column_count']} | {p['memory_mb']:.2f} MB | {p['duplicate_rows']:,} ({p['duplicate_pct']}%) |"
        )

    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## Detailed Table Schemas")
    md_lines.append("")

    for p in profiles:
        md_lines.append(f"### Table: `{p['table_name']}`")
        md_lines.append(f"- **Dimensions**: {p['row_count']:,} rows × {p['column_count']} columns")
        md_lines.append(f"- **Memory Footprint**: {p['memory_mb']:.2f} MB")
        md_lines.append(f"- **Duplicate Rows**: {p['duplicate_rows']:,}")
        md_lines.append("")
        md_lines.append("| Column Name | Type | Null Count | Null % | Unique Values | Key? | Sample Values |")
        md_lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

        for c in p["columns"]:
            key_badge = "**YES (PK)**" if c["is_candidate_key"] else "No"
            sample_clean = c["sample_values"].replace("|", "\\|")
            md_lines.append(
                f"| `{c['column_name']}` | `{c['data_type']}` | {c['null_count']:,} | {c['null_pct']}% | {c['unique_count']:,} | {key_badge} | `{sample_clean}` |"
            )
        md_lines.append("")

    content = "\n".join(md_lines)
    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        logger.info(f"Data dictionary saved to {out}")

    return content
