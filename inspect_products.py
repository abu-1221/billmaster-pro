
import sqlite3
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'billmaster.db')

def inspect_products():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, name, image_url FROM products")
    products = c.fetchall()
    
    print(f"Total products: {len(products)}")
    for p in products:
        print(f"ID: {p[0]} | Name: {p[1]} | URL: {p[2]}")
        
    conn.close()

if __name__ == "__main__":
    inspect_products()
