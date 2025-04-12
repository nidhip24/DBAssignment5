import pandas as pd
from database import engine

# Load CSV into DataFrame
df = pd.read_csv('/workspaces/DBAssignment5/archive/olist_orders_dataset.csv')

# Write to MySQL
df.to_sql('orders', con=engine, if_exists='append', index=False)

print(f"Loaded {len(df)} rows into olist_orders_dataset.")
