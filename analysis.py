"""
Steps 2 & 3: Ask questions of the data with SQL, then make charts.

Run after load_data.py:  python analysis.py
Charts are saved into a folder called charts/
"""

import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_FILE = "dc_311.db"
os.makedirs("charts", exist_ok=True)
conn = sqlite3.connect(DB_FILE)


def run(title, sql):
    """Run a SQL query, print the result, and return it as a DataFrame."""
    result = pd.read_sql_query(sql, conn)
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print(result.to_string(index=False))
    return result


# Q1. How many requests are there in total?
run("Q1. Total requests", """
    SELECT COUNT(*) AS total_requests
    FROM requests;
""")

# Q2. What are the 10 most common types of requests?
top_types = run("Q2. Top 10 request types", """
    SELECT servicecodedescription AS request_type,
           COUNT(*) AS num_requests
    FROM requests
    GROUP BY servicecodedescription
    ORDER BY num_requests DESC
    LIMIT 10;
""")

# Q3. Which wards submit the most requests?
by_ward = run("Q3. Requests by ward", """
    SELECT ward,
           COUNT(*) AS num_requests
    FROM requests
    WHERE ward IS NOT NULL
    GROUP BY ward
    ORDER BY ward;
""")

# Q4. How many days does it take on average to close each common request type?
#     julianday() turns a date into a number of days, so subtracting gives days between.
run("Q4. Average days to resolve (top 10 types, min 500 requests)", """
    SELECT servicecodedescription AS request_type,
           COUNT(*) AS closed_requests,
           ROUND(AVG(julianday(resolutiondate) - julianday(serviceorderdate)), 1) AS avg_days
    FROM requests
    WHERE resolutiondate IS NOT NULL
      AND serviceorderdate IS NOT NULL
      AND julianday(resolutiondate) >= julianday(serviceorderdate)
    GROUP BY servicecodedescription
    HAVING COUNT(*) >= 500
    ORDER BY avg_days DESC
    LIMIT 10;
""")

# Q5. How do requests change month by month?
by_month = run("Q5. Requests per month", """
    SELECT strftime('%Y-%m', serviceorderdate) AS month,
           COUNT(*) AS num_requests
    FROM requests
    WHERE serviceorderdate IS NOT NULL
    GROUP BY month
    ORDER BY month;
""")

# Q6. What is the #1 request type in each ward?
#     A subquery counts types per ward; the outer query keeps the biggest one.
run("Q6. Most common request type in each ward", """
    SELECT ward, request_type, num_requests
    FROM (
        SELECT ward,
               servicecodedescription AS request_type,
               COUNT(*) AS num_requests,
               RANK() OVER (PARTITION BY ward ORDER BY COUNT(*) DESC) AS rnk
        FROM requests
        WHERE ward IS NOT NULL
        GROUP BY ward, servicecodedescription
    )
    WHERE rnk = 1
    ORDER BY ward;
""")

conn.close()

# ---------- Charts ----------

# Chart 1: top request types (horizontal bar so long names fit)
plt.figure(figsize=(10, 6))
plt.barh(top_types["request_type"][::-1], top_types["num_requests"][::-1])
plt.title("Top 10 DC 311 Request Types (2025)")
plt.xlabel("Number of requests")
plt.tight_layout()
plt.savefig("charts/top_request_types.png", dpi=150)

# Chart 2: requests by ward
plt.figure(figsize=(8, 5))
plt.bar(by_ward["ward"].astype(str), by_ward["num_requests"])
plt.title("DC 311 Requests by Ward (2025)")
plt.xlabel("Ward")
plt.ylabel("Number of requests")
plt.tight_layout()
plt.savefig("charts/requests_by_ward.png", dpi=150)

# Chart 3: requests per month
plt.figure(figsize=(10, 5))
plt.plot(by_month["month"], by_month["num_requests"], marker="o")
plt.title("DC 311 Requests per Month (2025)")
plt.xlabel("Month")
plt.ylabel("Number of requests")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/requests_per_month.png", dpi=150)

print("\nCharts saved in the charts/ folder.")
