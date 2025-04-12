import pandas as pd
import time
import traceback
from database import engine

def run_query(label, query):
    try:
        start = time.time()
        df = pd.read_sql(query, con=engine)
        duration = time.time() - start
        print(f"[{label}] Time: {duration:.6f} sec")
        print(df)
        print()
    except Exception as e:
        print(f"[{label}] FAILED: {e}")
        traceback.print_exc()

queries = {
    "Total number of orders": "SELECT COUNT(*) AS total_orders FROM orders;",
    "Orders with NULL delivery date": "SELECT COUNT(*) AS undelivered_orders FROM orders WHERE order_delivered_customer_date IS NULL;",
    "Orders marked as delivered": "SELECT COUNT(*) AS delivered_orders FROM orders WHERE order_status = 'delivered';",
    "Distinct order statuses": "SELECT DISTINCT order_status FROM orders;"
}

print("\n== SCALAR FIELD TESTS ON orders TABLE ==")
for label, sql in queries.items():
    run_query(label, sql)
