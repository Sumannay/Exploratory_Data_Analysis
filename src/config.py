"""Centralized Configuration for InsightLab Platform.

Provides deterministic paths, database configurations, analytical constants,
and design system visual tokens across the entire pipeline.
"""

from pathlib import Path
import os

# Project Root Directory (robust resolution independent of execution cwd)
BASE_DIR = Path(__file__).resolve().parent.parent

# Data Directories
DATA_DIR = BASE_DIR / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_INTERIM_DIR = DATA_DIR / "interim"
DATA_PROCESSED_DIR = DATA_DIR / "processed"

# Outputs & Reports Directories
OUTPUTS_DIR = BASE_DIR / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
TABLES_DIR = OUTPUTS_DIR / "tables"
REPORTS_DIR = BASE_DIR / "reports"
SQL_DIR = BASE_DIR / "sql"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

# Ensure runtime directories exist
for directory in [DATA_RAW_DIR, DATA_INTERIM_DIR, DATA_PROCESSED_DIR, FIGURES_DIR, TABLES_DIR, REPORTS_DIR, SQL_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Database paths
DUCKDB_PATH = DATA_PROCESSED_DIR / "insightlab.duckdb"

# Raw Olist File Mappings
RAW_TABLE_FILES = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
    "marketing_leads": "olist_marketing_qualified_leads_dataset.csv",
    "closed_deals": "olist_closed_deals_dataset.csv"
}

# Remote Download URLs (Reliable GitHub mirror for automated zero-friction ingestion)
RAW_DOWNLOAD_URLS = {
    "olist_customers_dataset.csv": "https://raw.githubusercontent.com/mara/mara-olist-ecommerce-data/master/data/olist-ecommerce/olist_customers_dataset.csv",
    "olist_orders_dataset.csv": "https://raw.githubusercontent.com/mara/mara-olist-ecommerce-data/master/data/olist-ecommerce/olist_orders_dataset.csv",
    "olist_order_items_dataset.csv": "https://raw.githubusercontent.com/mara/mara-olist-ecommerce-data/master/data/olist-ecommerce/olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv": "https://raw.githubusercontent.com/mara/mara-olist-ecommerce-data/master/data/olist-ecommerce/olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv": "https://raw.githubusercontent.com/mara/mara-olist-ecommerce-data/master/data/olist-ecommerce/olist_order_reviews_dataset.csv",
    "olist_products_dataset.csv": "https://raw.githubusercontent.com/mara/mara-olist-ecommerce-data/master/data/olist-ecommerce/olist_products_dataset.csv",
    "olist_sellers_dataset.csv": "https://raw.githubusercontent.com/mara/mara-olist-ecommerce-data/master/data/olist-ecommerce/olist_sellers_dataset.csv",
    "product_category_name_translation.csv": "https://raw.githubusercontent.com/mara/mara-olist-ecommerce-data/master/data/olist-ecommerce/product_category_name_translation.csv",
    "olist_marketing_qualified_leads_dataset.csv": "https://raw.githubusercontent.com/mara/mara-olist-ecommerce-data/master/data/olist-marketing-funnel/olist_marketing_qualified_leads_dataset.csv",
    "olist_closed_deals_dataset.csv": "https://raw.githubusercontent.com/mara/mara-olist-ecommerce-data/master/data/olist-marketing-funnel/olist_closed_deals_dataset.csv"
}

# Design System & Visual Palette (Executive Modern Slate Theme)
COLOR_PALETTE = {
    "primary": "#2563EB",       # Royal Blue
    "secondary": "#0D9488",     # Teal
    "accent": "#F59E0B",        # Amber Gold
    "danger": "#EF4444",        # Crimson Red
    "success": "#10B981",       # Emerald Green
    "dark": "#1E293B",          # Slate Dark
    "light": "#F8FAFC",         # Slate 50
    "grid": "#E2E8F0",          # Slate 200
    "sequential": ["#E0F2FE", "#BAE6FD", "#7DD3FC", "#38BDF8", "#0284C7", "#0369A1", "#075985"],
    "diverging": ["#EF4444", "#F87171", "#FCA5A5", "#E2E8F0", "#86EFAC", "#4ADE80", "#22C55E"]
}

# Analytical Constants
RANDOM_STATE = 42
TARGET_CURRENCY = "BRL"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
