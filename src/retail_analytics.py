"""Data generator and feature engineering for Customer Retail Analytics.

Generates the high-fidelity customer segmentation and retail analytics dataset
that powers the 3 executive dashboards matching the exact business metrics:
- 9,994 transactions, 793 customers
- Top customers: Sean Miller, Tamara Chand, Raymond Buch, Tom Ashbrook, etc.
- Standard segments: Champions, Loyal Customers, Potential Loyalists, At Risk, Lost Customers/Others
- US States, Cities, Regions, Age brackets, Gender, Categories, Discounts, and Quantities
"""

from pathlib import Path
import numpy as np
import pandas as pd

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
RETAIL_DATA_FILE = PROCESSED_DIR / "retail_customer_analytics.csv"
RFM_SUMMARY_FILE = PROCESSED_DIR / "customer_rfm_summary.csv"


def build_retail_customer_dataset() -> pd.DataFrame:
    """Build the comprehensive retail customer dataset matching the exact target metrics."""
    np.random.seed(42)

    # 1. Exact Anchor Customers from Dashboard 3 Table & Bar Chart
    top_ranked_customers = [
        {"name": "Sean Miller", "sales": 25043.1, "freq": 24, "city": "Jacksonville", "state": "FL", "region": "South", "recency": 12, "segment": "Champion"},
        {"name": "Tamara Chand", "sales": 19052.2, "freq": 18, "city": "Seattle", "state": "WA", "region": "West", "recency": 8, "segment": "Champion"},
        {"name": "Raymond Buch", "sales": 15117.3, "freq": 16, "city": "New York City", "state": "NY", "region": "Northeast", "recency": 15, "segment": "Champion"},
        {"name": "Tom Ashbrook", "sales": 14595.6, "freq": 15, "city": "Los Angeles", "state": "CA", "region": "West", "recency": 22, "segment": "Champion"},
        {"name": "Adrian Barton", "sales": 14473.6, "freq": 19, "city": "Detroit", "state": "MI", "region": "Midwest", "recency": 14, "segment": "Champion"},
        {"name": "Ken Lonsdale", "sales": 14175.2, "freq": 21, "city": "Chicago", "state": "IL", "region": "Midwest", "recency": 19, "segment": "Champion"},
        {"name": "Sanjit Chand", "sales": 14142.3, "freq": 17, "city": "Philadelphia", "state": "PA", "region": "Northeast", "recency": 25, "segment": "Champion"},
        {"name": "Hunter Lopez", "sales": 12873.3, "freq": 14, "city": "San Francisco", "state": "CA", "region": "West", "recency": 30, "segment": "Loyal Customer"},
        {"name": "Sanjit Engle", "sales": 12209.4, "freq": 16, "city": "Houston", "state": "TX", "region": "South", "recency": 28, "segment": "Loyal Customer"},
    ]

    # Exact table rows from Image 3
    table_anchors = [
        {"name": "Aaron Bergman", "sales": 886.2, "freq": 6, "city": "Arlington", "state": "TX", "region": "South", "recency": 416, "segment": "At Risk"},
        {"name": "Aaron Hawkins", "sales": 1744.7, "freq": 11, "city": "Los Angeles", "state": "CA", "region": "West", "recency": 13, "segment": "Loyal Customer"},
        {"name": "Aaron Smayling", "sales": 3050.7, "freq": 10, "city": "New York City", "state": "NY", "region": "Northeast", "recency": 89, "segment": "Others"},
        {"name": "Adam Bellavance", "sales": 7755.6, "freq": 18, "city": "Houston", "state": "TX", "region": "South", "recency": 55, "segment": "Potential Loyalist"},
        {"name": "Adam Hart", "sales": 3250.3, "freq": 20, "city": "Philadelphia", "state": "PA", "region": "Northeast", "recency": 35, "segment": "Potential Loyalist"}
    ]

    known_anchors = {c["name"]: c for c in (top_ranked_customers + table_anchors)}

    # Pool of cities matching exact counts in Image 3
    city_targets = [
        ("New York City", "NY", "Northeast", 355),
        ("Los Angeles", "CA", "West", 284),
        ("Philadelphia", "PA", "Northeast", 236),
        ("San Francisco", "CA", "West", 192),
        ("Seattle", "WA", "West", 188),
        ("Houston", "TX", "South", 122),
        ("Chicago", "IL", "Midwest", 98),
        ("Detroit", "MI", "Midwest", 74),
        ("Jacksonville", "FL", "South", 55),
        ("Columbus", "OH", "Midwest", 42),
        ("San Diego", "CA", "West", 38),
        ("Dallas", "TX", "South", 34)
    ]
    city_names = [c[0] for c in city_targets]
    city_probs = [c[3] for c in city_targets]
    city_probs = [p / sum(city_probs) for p in city_probs]
    city_lookup = {c[0]: c for c in city_targets}

    # Generate customer names to reach exactly 793 customers
    first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
                   "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen",
                   "Daniel", "Matthew", "Anthony", "Donald", "Mark", "Paul", "Steven", "Andrew", "Kenneth", "Joshua",
                   "Ashley", "Kimberly", "Emily", "Donna", "Michelle", "Dorothy", "Carol", "Amanda", "Melissa", "Deborah"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                  "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
                  "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
                  "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"]

    customer_names = list(known_anchors.keys())
    while len(customer_names) < 793:
        cand = f"{np.random.choice(first_names)} {np.random.choice(last_names)}"
        if cand not in customer_names:
            customer_names.append(cand)

    # Categories matching Image 1 & Image 3
    categories = [
        "Mobiles & Tablets",
        "Appliances",
        "Entertainment",
        "Computing",
        "Men's Fashion",
        "Women's Fashion",
        "Beauty & Grooming",
        "Superstore",
        "Home & Living",
        "Kids & Baby",
        "Soghaat",
        "School & Education"
    ]

    # Pre-assign segments to hit target percentages:
    # Champions: ~4.29% (approx 34 customers)
    # Loyal Customers: ~18.41% (approx 146 customers)
    # Potential Loyalists: ~19.67% (approx 156 customers)
    # At Risk: ~28.88% (approx 229 customers)
    # Others / Lost: ~28.75% (approx 228 customers)
    target_segments = (
        ["Champion"] * 34 +
        ["Loyal Customer"] * 146 +
        ["Potential Loyalist"] * 156 +
        ["At Risk"] * 229 +
        ["Others"] * (793 - (34 + 146 + 156 + 229))
    )
    np.random.shuffle(target_segments)

    customer_profiles = {}
    for idx, name in enumerate(customer_names):
        if name in known_anchors:
            anch = known_anchors[name]
            city_info = city_lookup.get(anch["city"], (anch["city"], anch["state"], anch["region"], 100))
            seg = anch["segment"]
            rec = anch["recency"]
            c_type = "Returning"
        else:
            chosen_city_name = np.random.choice(city_names, p=city_probs)
            city_info = city_lookup[chosen_city_name]
            seg = target_segments[idx]
            rec = int(np.random.choice(
                [15, 45, 95, 210, 420],
                p=[0.25, 0.25, 0.20, 0.15, 0.15]
            ) + np.random.randint(-10, 10))
            rec = max(2, rec)
            c_type = "New" if np.random.rand() < 0.232 else "Returning"

        age = int(np.random.choice([19, 26, 35, 45, 54, 63, 74], p=[0.06, 0.21, 0.29, 0.22, 0.12, 0.07, 0.03]))
        gender = np.random.choice(["Male", "Female"], p=[0.52, 0.48])

        customer_profiles[name] = {
            "customer_id": f"CUST-{1000 + idx}",
            "customer_name": name,
            "city": city_info[0],
            "state": city_info[1],
            "region": city_info[2],
            "customer_type": c_type,
            "age": age,
            "gender": gender,
            "segment": seg,
            "recency": rec
        }

    # Order Generation: Exactly 9,994 orders
    # Date bounds: 2020-10-01 to 2021-09-30
    start_date = pd.Timestamp("2020-10-01")
    end_date = pd.Timestamp("2021-09-30")
    total_days = (end_date - start_date).days

    orders = []
    # Guarantee anchor frequencies
    for name, anch in known_anchors.items():
        prof = customer_profiles[name]
        freq = anch["freq"]
        tot_sales = anch["sales"]
        for o_i in range(freq):
            cat = np.random.choice(categories)
            rand_day = np.random.randint(0, total_days)
            o_date = start_date + pd.Timedelta(days=rand_day)
            disc = float(np.random.choice([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]))
            qty = np.random.randint(1, 15)
            orders.append({
                "order_id": f"ORD-{100000 + len(orders)}",
                "customer_name": name,
                "customer_id": prof["customer_id"],
                "order_date": o_date.strftime("%Y-%m-%d"),
                "order_month": o_date.strftime("%B %Y"),
                "year_month": o_date.strftime("%Y-%m"),
                "category": cat,
                "city": prof["city"],
                "state": prof["state"],
                "region": prof["region"],
                "customer_type": prof["customer_type"],
                "gender": prof["gender"],
                "age": prof["age"],
                "discount_percent": int(disc * 100),
                "quantity": qty,
                "sales_amount": round(tot_sales / freq, 2)
            })

    # Distribute the remaining orders among other customers
    remaining_orders_count = 9994 - len(orders)
    other_customers = [n for n in customer_names if n not in known_anchors]
    order_weights = np.random.exponential(scale=2.0, size=len(other_customers))
    order_weights = order_weights / order_weights.sum()

    assigned_counts = np.random.multinomial(remaining_orders_count, order_weights)
    for c_idx, name in enumerate(other_customers):
        prof = customer_profiles[name]
        cnt = assigned_counts[c_idx]
        if cnt <= 0:
            cnt = 1
        for _ in range(cnt):
            cat = np.random.choice(categories)
            # Give June 2021 a higher weight to create the $2.4M peak shown in Image 1
            if np.random.rand() < 0.22:
                o_date = pd.Timestamp("2021-06-01") + pd.Timedelta(days=np.random.randint(0, 29))
            else:
                o_date = start_date + pd.Timedelta(days=np.random.randint(0, total_days))

            disc = float(np.random.choice([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
                                          p=[0.30, 0.15, 0.20, 0.12, 0.10, 0.06, 0.04, 0.03]))
            qty = int(np.random.choice(np.arange(1, 21), p=np.linspace(20, 1, 20)/sum(np.linspace(20, 1, 20))))
            base = {"Mobiles & Tablets": 420, "Appliances": 280, "Entertainment": 190, "Computing": 460,
                    "Men's Fashion": 65, "Women's Fashion": 75, "Beauty & Grooming": 45, "Superstore": 40,
                    "Home & Living": 85, "Kids & Baby": 50, "Soghaat": 30, "School & Education": 25}.get(cat, 50)
            item_val = round(base * np.random.uniform(0.7, 1.3) * (qty ** 0.5) * (1.0 - disc), 2)

            orders.append({
                "order_id": f"ORD-{100000 + len(orders)}",
                "customer_name": name,
                "customer_id": prof["customer_id"],
                "order_date": o_date.strftime("%Y-%m-%d"),
                "order_month": o_date.strftime("%B %Y"),
                "year_month": o_date.strftime("%Y-%m"),
                "category": cat,
                "city": prof["city"],
                "state": prof["state"],
                "region": prof["region"],
                "customer_type": prof["customer_type"],
                "gender": prof["gender"],
                "age": prof["age"],
                "discount_percent": int(disc * 100),
                "quantity": qty,
                "sales_amount": item_val
            })

    # Exactly 9,994 orders
    if len(orders) > 9994:
        orders = orders[:9994]
    elif len(orders) < 9994:
        shortage = 9994 - len(orders)
        for i in range(shortage):
            dup = dict(orders[i])
            dup["order_id"] = f"ORD-{200000 + i}"
            orders.append(dup)

    df_tx = pd.DataFrame(orders)

    # Save transaction dataset
    df_tx.to_csv(RETAIL_DATA_FILE, index=False)
    print(f"Saved {len(df_tx)} retail transactions to {RETAIL_DATA_FILE}")

    # Build RFM Summary table
    rfm_rows = []
    for name, prof in customer_profiles.items():
        c_orders = df_tx[df_tx["customer_name"] == name]
        if len(c_orders) > 0:
            monetary = round(c_orders["sales_amount"].sum(), 1)
            freq = len(c_orders)
        else:
            monetary = 150.0
            freq = 1

        rec = prof["recency"]
        # Override known anchor numbers
        if name in known_anchors:
            monetary = known_anchors[name]["sales"]
            freq = known_anchors[name]["freq"]
            rec = known_anchors[name]["recency"]
            seg = known_anchors[name]["segment"]
        else:
            seg = prof["segment"]

        rfm_rows.append({
            "customer_name": name,
            "Monetary": monetary,
            "Frequency": freq,
            "Sum_of_Recency": rec,
            "Segment": seg,
            "city": prof["city"],
            "state": prof["state"],
            "region": prof["region"],
            "customer_type": prof["customer_type"],
            "age": prof["age"],
            "gender": prof["gender"]
        })

    rfm_summary = pd.DataFrame(rfm_rows)
    rfm_summary.sort_values(by="Monetary", ascending=False, inplace=True)
    rfm_summary.to_csv(RFM_SUMMARY_FILE, index=False)
    print(f"Saved {len(rfm_summary)} customer RFM profiles to {RFM_SUMMARY_FILE}")

    return df_tx


if __name__ == "__main__":
    build_retail_customer_dataset()
