import json
import os

import numpy as np
import pandas as pd

SEED = 42
ROWS = 200
rng = np.random.default_rng(SEED)

names = [
    "Ravi Sharma", "Priya Mehta", "Amit Verma", "Neha Gupta", "Rahul Singh",
    "Sneha Iyer", "Vikram Rao", "Kavya Nair", "Arjun Das", "Pooja Joshi",
    "Rohit Kapoor", "Ananya Roy", "Karan Malhotra", "Divya Pillai",
]
categories = ["Food", "Electronics", "Clothing", "Furniture"]

dates = pd.Timestamp("2026-01-01") + pd.to_timedelta(rng.integers(0, 90, ROWS), unit="D")

df = pd.DataFrame({
    "order_id": np.arange(1001, 1001 + ROWS),
    "date": dates,
    "customer": rng.choice(names, ROWS),
    "category": rng.choice(categories, ROWS),
    "amount": rng.integers(100, 20000, ROWS),
})

# Mess 1: dates written 3 different ways
formats = ["%Y-%m-%d", "%d/%m/%Y", "%B %d %Y"]
pick = rng.integers(0, 3, ROWS)
df["date"] = [d.strftime(formats[p]) for d, p in zip(df["date"], pick)]

# Mess 2: category spelled Food / food / FOOD
case = rng.integers(0, 3, ROWS)
df["category"] = [
    c if k == 0 else c.lower() if k == 1 else c.upper()
    for c, k in zip(df["category"], case)
]

# Mess 3: extra spaces around some names
df["customer"] = df["customer"].astype(object)
space_rows = rng.choice(ROWS, 15, replace=False)
df.loc[space_rows, "customer"] = "  " + df.loc[space_rows, "customer"] + " "

# Mess 4: some amounts written as text like "₹2,500"
df["amount"] = df["amount"].astype(object)
rupee_rows = rng.choice(ROWS, 20, replace=False)
df.loc[rupee_rows, "amount"] = [f"₹{int(v):,}" for v in df.loc[rupee_rows, "amount"]]

# Mess 5: some amounts missing
others = np.setdiff1d(np.arange(ROWS), rupee_rows)
missing_rows = rng.choice(others, 8, replace=False)
df.loc[missing_rows, "amount"] = np.nan

# Mess 6: some rows copied twice, then shuffle
dup_rows = rng.choice(ROWS, 10, replace=False)
df = pd.concat([df, df.loc[dup_rows]], ignore_index=True)
df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)

os.makedirs("datasets", exist_ok=True)
df.to_csv("datasets/sample_sales.csv", index=False)

amount_text = df["amount"].astype(str)
answer_key = {
    "total_rows": int(len(df)),
    "real_orders": ROWS,
    "duplicate_rows": int(df.duplicated().sum()),
    "missing_amounts": int(df["amount"].isna().sum()),
    "rupee_text_amounts": int(amount_text.str.startswith("₹").sum()),
    "names_with_extra_spaces": int((df["customer"] != df["customer"].str.strip()).sum()),
    "category_spellings": sorted(df["category"].unique().tolist()),
    "date_formats_used": 3,
}

with open("datasets/answer_key.json", "w") as f:
    json.dump(answer_key, f, indent=2, ensure_ascii=False)

print("Saved datasets/sample_sales.csv")
print(json.dumps(answer_key, indent=2, ensure_ascii=False))
