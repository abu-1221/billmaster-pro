"""
Perfect South Indian Menu - Final Verified Version
"""
import sqlite3
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'billmaster.db')

def show_menu():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("🍱 CURRENT VERIFIED SOUTH INDIAN MENU:")
    print("-" * 50)
    c.execute("SELECT name, image_url FROM products")
    for row in c.fetchall():
        print(f"✔️ {row[0]:<25} | {row[1]}")
    
    conn.close()

if __name__ == '__main__':
    show_menu()
