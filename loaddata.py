import mysql.connector
#from dotenv import load_dotenv
import csv

conn = mysql.connector.connect(
    host='127.0.0.1',
    user="dbowner",
    password="Secret5555",          
    database='order_db'
)

cursor = conn.cursor()
sql = "INSERT INTO orders (order_id, customer_id, order_status, order_purchase_timestamp,  order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)";

with open("archive/olist_orders_dataset.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    for i, line in enumerate(reader):
        if i != 0:
            cursor.execute(sql, line)
conn.commit()

cursor.close()
conn.close()