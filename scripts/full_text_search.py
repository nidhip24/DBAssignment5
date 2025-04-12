import pandas as pd
import time
import traceback
from sqlalchemy import text
from database import engine

search_term = 'delivered'

def run_query(label, query, params=None):
    start = time.time()
    try:
        df = pd.read_sql(query, con=engine, params=params)
        duration = time.time() - start
        print(f"[{label}] Time taken: {duration:.6f} seconds | Rows: {len(df)}")
        return df
    except Exception as e:
        print(f"[{label}] FAILED: {e}")
        traceback.print_exc()
        return None

# 1. Run LIKE query BEFORE index
print("== BEFORE CREATING FULLTEXT INDEX ==")
like_query = text("SELECT * FROM orders WHERE order_status LIKE :pattern")
run_query("LIKE search (no index)", like_query, params={"pattern": f"%{search_term}%"})

# 2. Create FULLTEXT index
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE orders ADD FULLTEXT(order_status);"))
        print("Full-text index created.")
    except Exception as e:
        print("Index creation error (possibly already exists):", e)

print("Sleeping 5 seconds before MATCH search...\n")
time.sleep(5)

# 3. Run MATCH...AGAINST query
print("\n== AFTER CREATING FULLTEXT INDEX ==")
match_query = text("SELECT * FROM orders WHERE MATCH(order_status) AGAINST(:term IN NATURAL LANGUAGE MODE)")
run_query("MATCH ... AGAINST", match_query, params={"term": search_term})
