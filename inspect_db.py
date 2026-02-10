import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'billmaster.db')

def inspect():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("--- Categories ---")
    c.execute("SELECT id, name FROM categories")
    for row in c.fetchall():
        print(row)
        
    print("\n--- Products missing real looking URLs ---")
    c.execute("SELECT id, name, image_url FROM products WHERE image_url IS NULL OR length(image_url) < 5")
    rows = c.fetchall()
    for row in rows:
        print(row)
    
    if rows:
        print(f"\nCleaning up {len(rows)} items...")
        c.execute("DELETE FROM products WHERE image_url IS NULL OR length(image_url) < 5")
        conn.commit()
    else:
        print("\nNo items missing pictures found.")
        
    conn.close()

if __name__ == '__main__':
    inspect()
