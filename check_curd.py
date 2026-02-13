import sqlite3
import os

db = os.path.join('database', 'billmaster.db')
conn = sqlite3.connect(db)
c = conn.cursor()
c.execute("SELECT name, image_url FROM products WHERE name LIKE '%Curd Rice%'")
for row in c.fetchall():
    print(f"Product: {row[0]}")
    print(f"Image: {row[1]}")
conn.close()
