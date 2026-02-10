import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'billmaster.db')

def cleanup():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Check for empty, null, or common placeholder strings
    query = "DELETE FROM products WHERE image_url IS NULL OR image_url = '' OR image_url LIKE '%placeholder%'"
    c.execute(query)
    count = c.rowcount
    
    conn.commit()
    conn.close()
    
    print(f"✅ Successfully removed {count} food items that did not have valid pictures.")

if __name__ == '__main__':
    cleanup()
