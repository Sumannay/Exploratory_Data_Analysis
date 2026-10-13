"""Script to construct notebooks/01_data_understanding.ipynb."""

import json
from pathlib import Path

notebook_content = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# InsightLab — 01: Data Understanding & Initial Relational Profiling\n",
                "\n",
                "**Role**: Senior Data Scientist / Analytics Engineer  \n",
                "**Dataset**: Olist Brazilian E-Commerce (~100k Orders, Relational Fact/Dimension Tables)  \n",
                "**Objective**: Conduct systematic data ingestion, assess dimensions, inspect column types, verify candidate primary/foreign keys, and profile baseline data quality before applying transformations.\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import sys\n",
                "from pathlib import Path\n",
                "\n",
                "# Add project root to sys.path\n",
                "ROOT_DIR = Path(\"..\").resolve()\n",
                "if str(ROOT_DIR) not in sys.path:\n",
                "    sys.path.append(str(ROOT_DIR))\n",
                "\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "from src.config import DATA_RAW_DIR, RAW_TABLE_FILES\n",
                "from src.data_loader import discover_csv_files, load_all_raw_tables, profile_dataframe\n",
                "\n",
                "pd.set_option(\"display.max_columns\", 50)\n",
                "pd.set_option(\"display.width\", 1000)\n",
                "print(f\"Project root resolved: {ROOT_DIR}\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Discovered Raw Datasets\n",
                "Let's inspect the files present in `data/raw/` and their respective sizes on disk."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "catalog = discover_csv_files(DATA_RAW_DIR)\n",
                "catalog_df = pd.DataFrame([\n",
                "    {\"filename\": k, \"size_mb\": v[\"size_mb\"]}\n",
                "    for k, v in catalog.items()\n",
                "])\n",
                "catalog_df.sort_values(by=\"size_mb\", ascending=False)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Ingesting Relational Tables\n",
                "Load all tables into memory using our robust data loader."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "tables = load_all_raw_tables(DATA_RAW_DIR, RAW_TABLE_FILES)\n",
                "print(f\"Successfully loaded {len(tables)} tables:\", list(tables.keys()))"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. High-Level Inventory (Rows, Columns, Memory, Keys)\n",
                "Let's summarize table dimensions and candidate primary keys."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "profiles = [profile_dataframe(df, name) for name, df in tables.items()]\n",
                "summary = pd.DataFrame([{\n",
                "    \"Table\": p[\"table_name\"],\n",
                "    \"Rows\": f\"{p['row_count']:,}\",\n",
                "    \"Cols\": p[\"column_count\"],\n",
                "    \"Memory_MB\": p[\"memory_mb\"],\n",
                "    \"Duplicate_Rows\": p[\"duplicate_rows\"],\n",
                "    \"Candidate_PKs\": [c[\"column_name\"] for c in p[\"columns\"] if c[\"is_candidate_key\"]]\n",
                "} for p in profiles])\n",
                "summary"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Key Relational Integrity & Integrity Checks\n",
                "Let's inspect foreign key consistency between orders and customers, and check the unique customer vs order relationship."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "orders = tables[\"orders\"]\n",
                "customers = tables[\"customers\"]\n",
                "\n",
                "print(f\"Total Orders: {len(orders):,}\")\n",
                "print(f\"Unique order_id: {orders['order_id'].nunique():,}\")\n",
                "print(f\"Total Customers: {len(customers):,}\")\n",
                "print(f\"Unique customer_id: {customers['customer_id'].nunique():,}\")\n",
                "print(f\"Distinct Unique Customers (customer_unique_id): {customers['customer_unique_id'].nunique():,}\")\n",
                "\n",
                "# Check orphaned customer_id in orders\n",
                "missing_cust = ~orders[\"customer_id\"].isin(customers[\"customer_id\"])\n",
                "print(f\"Orders referencing non-existent customer_id: {missing_cust.sum()}\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Sample Preview of Core Fact Tables\n",
                "Review the schema and actual records from `orders`, `order_items`, and `payments`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "display(orders.head(3))\n",
                "display(tables[\"order_items\"].head(3))\n",
                "display(tables[\"payments\"].head(3))"
            ]
        }
    ],
    "metadata": {
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

output_path = Path(__file__).resolve().parent.parent / "notebooks" / "01_data_understanding.ipynb"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=2)

print(f"Created notebook at {output_path}")
