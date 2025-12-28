import requests
import csv
import time

# ===============================
# CONFIG
# ===============================
GRAPH_URL = "https://gateway.thegraph.com/api/5b4fc6ecb44d7f52beb3f5af2d701aff/subgraphs/id/JCNWRypm7FYwV8fx5HhzZPSFaMxgkPuw4TnR3Gpi81zk"

OUTPUT_BORROWS = r"D:\blockchain\borrows_full.csv"
OUTPUT_REPAYS = r"D:\blockchain\repays_full.csv"

PAGE_SIZE = 1000
SLEEP_SECONDS = 0.2  # avoid rate limits

# ===============================
# QUERY FUNCTIONS
# ===============================
def get_borrows_query(last_ts):
    return f"""
{{
  borrows(
    first: {PAGE_SIZE}
    orderBy: timestamp
    orderDirection: asc
    where: {{ timestamp_gt: {last_ts} }}
  ) {{
    id
    amountUSD
    timestamp
    account {{ id }}
    asset {{ id }}
  }}
}}
"""

def get_repays_query(last_ts):
    return f"""
{{
  repays(
    first: {PAGE_SIZE}
    orderBy: timestamp
    orderDirection: asc
    where: {{ timestamp_gt: {last_ts} }}
  ) {{
    id
    amountUSD
    timestamp
    account {{ id }}
    asset {{ id }}
  }}
}}
"""

# ===============================
# PAGINATION FUNCTION
# ===============================
def fetch_paginated(query_function, output_path, entity_name):
    last_ts = 0  # start as integer
    total_rows = 0

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = None

        while True:
            query = query_function(last_ts)
            response = requests.post(GRAPH_URL, json={"query": query})

            if response.status_code != 200:
                raise Exception(f"HTTP error {response.status_code}: {response.text}")

            data = response.json().get("data", {}).get(entity_name, [])

            if not data:
                print(f"✅ Finished {entity_name}. Total rows: {total_rows}")
                break

            # Initialize CSV header once
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=[
                    "id", "account_id", "asset_id", "amountUSD", "timestamp"
                ])
                writer.writeheader()

            for row in data:
                writer.writerow({
                    "id": row["id"],
                    "account_id": row["account"]["id"],
                    "asset_id": row["asset"]["id"],
                    "amountUSD": row["amountUSD"],
                    "timestamp": row["timestamp"]
                })

            last_ts = int(data[-1]["timestamp"])  # update last timestamp as integer
            total_rows += len(data)

            print(f"{entity_name}: fetched {total_rows} rows | last_ts={last_ts}")
            time.sleep(SLEEP_SECONDS)

# ===============================
# RUN
# ===============================
print("🚀 Fetching BORROWS...")
fetch_paginated(get_borrows_query, OUTPUT_BORROWS, "borrows")

print("\n🚀 Fetching REPAYS...")
fetch_paginated(get_repays_query, OUTPUT_REPAYS, "repays")

print("\n🎉 ALL DATA DOWNLOADED SUCCESSFULLY")
print("Saved to:")
print(OUTPUT_BORROWS)
print(OUTPUT_REPAYS)
