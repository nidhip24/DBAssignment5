import pandas as pd
import time
from database import engine
import traceback
from sqlalchemy import text

def time_query(label, query):
    start = time.time()
    df = pd.read_sql(query, con=engine)
    elapsed = time.time() - start
    print(f"[{label}] Time taken: {elapsed:.6f} seconds | Rows: {len(df)}")
    return elapsed

# Queries to benchmark
queries = {
    "Filter by order_status": "SELECT * FROM orders WHERE order_status = 'delivered';",
    "Filter by customer_id + order_status": "SELECT * FROM orders WHERE customer_id = '9ef432eb6251297304e76186b10a928d' AND order_status = 'delivered';"
}

# Step 1: Run queries BEFORE index
print("\n== BEFORE CREATING INDEXES ==")
before_times = {}
for label, sql in queries.items():
    before_times[label] = time_query(label, sql)

# Step 2: Create indexes
with engine.connect() as conn:
    for index_sql, idx_label in [
        ("CREATE INDEX idx_order_status ON orders(order_status);", "idx_order_status"),
        ("CREATE INDEX idx_customer_status ON orders(customer_id, order_status);", "idx_customer_status")
    ]:
        try:
            conn.execute(text(index_sql))  # ✅ wrap with text()
            print(f"Created: {idx_label}")
        except Exception as e:
            print(f"{idx_label} already exists or error:", e)
            traceback.print_exc()

# Step 3: Run queries AFTER index
print("\n== AFTER CREATING INDEXES ==")
after_times = {}
for label, sql in queries.items():
    after_times[label] = time_query(label, sql)

# Step 4: Show comparison
print("\n== TIME COMPARISON ==")
for label in queries:
    print(f"{label}:\n  Before: {before_times[label]:.6f} sec\n  After:  {after_times[label]:.6f} sec\n")
