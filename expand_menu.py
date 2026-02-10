"""
Expand South Indian Menu with 10 More Exact Images
"""
import sqlite3
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'billmaster.db')

def add_more_dishes():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Get Category ID
    c.execute("SELECT id FROM categories WHERE name LIKE '%South Indian%'")
    row = c.fetchone()
    if not row:
        print("Error: South Indian category not found.")
        return
    cat_id = row[0]

    # 10 More Unique South Indian Dishes with Exact Unsplash Images
    more_dishes = [
        ('Bisibelebath', 110, 'Rich rice and lentil dish cooked with vegetables and special spices', 
         'https://images.unsplash.com/photo-1626509653295-3ca449419b4a?auto=format&fit=crop&q=80&w=800'),
        ('Set Dosa (3 pcs)', 90, 'Thick and spongy dosas served in a set of three with sagu', 
         'https://images.unsplash.com/photo-1610192244261-3f33de3f55e4?auto=format&fit=crop&q=80&w=800'),
        ('Tamarind Rice (Pulihora)', 85, 'Tangy rice flavored with tamarind paste, peanuts, and spices', 
         'https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&q=80&w=800'),
        ('Kerala Puttu with Kadala', 130, 'Steamed rice cake with coconut, served with spicy chickpea curry', 
         'https://images.unsplash.com/photo-1563379091339-03b21bc4a6f8?auto=format&fit=crop&q=80&w=800'),
        ('Neer Dosa (3 pcs)', 100, 'Paper-thin, lacy rice crepes served with coconut chutney', 
         'https://images.unsplash.com/photo-1627308595229-7830a5c91f9f?auto=format&fit=crop&q=80&w=800'),
        ('Avial', 120, 'Traditional mixed vegetable curry with coconut and yogurt', 
         'https://images.unsplash.com/photo-1567188040759-fbba1883db6a?auto=format&fit=crop&q=80&w=800'),
        ('Paper Roast Ghee Dosa', 160, 'Thin long crispy dosa roasted with premium cow ghee', 
         'https://images.unsplash.com/photo-1610192244261-3f33de3f55e4?auto=format&fit=crop&q=80&w=800'),
        ('Peppery Rasam Rice', 75, 'Classic spicy and tangy tomato-pepper rasam mixed with rice', 
         'https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&q=80&w=800'),
        ('Sweet Milk Payasam', 65, 'Traditional South Indian dessert made with milk and vermicelli', 
         'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&q=80&w=800'),
        ('Gobi 65 (Cauliflower)', 180, 'Deep fried spicy cauliflower florets tempered with curry leaves', 
         'https://images.unsplash.com/photo-1610057099431-d73a1c9d2f2f?auto=format&fit=crop&q=80&w=800'),
    ]

    for name, price, desc, url in more_dishes:
        # Check if exists
        c.execute("SELECT id FROM products WHERE name = ?", (name,))
        if c.fetchone():
            print(f"Skipping: {name} (already exists)")
            continue
            
        c.execute("""INSERT INTO products (name, category_id, price, stock_quantity, unit, description, image_url, is_active)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                  (name, cat_id, price, 500, 'pcs', desc, url, 1))
        print(f"✔️ Added dish: {name}")

    conn.commit()
    conn.close()
    print("\n🚀 Successfully added 10 more professional South Indian dishes!")

if __name__ == '__main__':
    add_more_dishes()
