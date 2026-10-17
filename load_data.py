"""
Step 1: Load DC 311 service request data into a SQLite database.

Download the CSV first:
  https://opendata.dc.gov/datasets/DCGIS::311-city-service-requests-in-2025
  (click Download -> CSV), then save it in this folder as  dc_311_2025.csv

Run:  python load_data.py
"""

import sqlite3
import pandas as pd

CSV_FILE = "dc_311_2025.csv"
DB_FILE = "dc_311.db"

# The columns this project uses (lowercase names).
COLUMNS_NEEDED = [
    "servicerequestid",
    "servicecodedescription",     # what the request was about, e.g. "Bulk Collection"
    "servicetypecodedescription", # the broader category / agency group
    "ward",                       # DC is split into 8 wards
    "serviceorderdate",           # when the request was made
    "resolutiondate",             # when it was closed
    "serviceorderstatus",         # e.g. CLOSED, OPEN
]

# 1. Read the CSV into a pandas DataFrame (a table in memory)
print(f"Reading {CSV_FILE} ...")
df = pd.read_csv(CSV_FILE, low_memory=False)

# 2. Make all column names lowercase so they're easy to type in SQL
df.columns = [c.strip().lower() for c in df.columns]

missing = [c for c in COLUMNS_NEEDED if c not in df.columns]
if missing:
    print("These expected columns weren't found:", missing)
    print("Columns in your file are:", list(df.columns))
    print("Rename them in COLUMNS_NEEDED above to match, then run again.")
    raise SystemExit(1)

df = df[COLUMNS_NEEDED]

# 3. Clean the data
#    - turn date text into real dates, then store them in a standard format
for col in ["serviceorderdate", "resolutiondate"]:
    df[col] = pd.to_datetime(df[col], errors="coerce", utc=True).dt.strftime("%Y-%m-%d %H:%M:%S")

#    - make ward a clean whole number. The file may store it as "Ward 1" or "1",
#      so pull out just the digits. Some rows are blank.
df["ward"] = pd.to_numeric(
    df["ward"].astype(str).str.extract(r"(\d+)")[0], errors="coerce"
).astype("Int64")
print("Requests with a ward:", df["ward"].notna().sum())

#    - keep only requests made in 2025 (a few late rows spill into 2026)
df = df[df["serviceorderdate"].str.startswith("2025", na=False)]

#    - drop exact duplicate requests
before = len(df)
df = df.drop_duplicates(subset="servicerequestid")
print(f"Removed {before - len(df)} duplicate rows.")

# 4. Save it into a SQLite database table called "requests"
conn = sqlite3.connect(DB_FILE)
df.to_sql("requests", conn, if_exists="replace", index=False)
conn.close()

print(f"Done! Loaded {len(df):,} requests into {DB_FILE} (table: requests).")
