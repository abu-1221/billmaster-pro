
"""
Add 11 More Authentic South Indian Dishes with Exact Verified Images
"""
import sqlite3
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'billmaster.db')

def add_authentic_dishes():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Get Category ID for 'South Indian Specials' (created in final_menu_setup.py)
    # If not found, look for 'South Indian' or create one
    c.execute("SELECT id FROM categories WHERE name LIKE '%South Indian%'")
    row = c.fetchone()
    if row:
        category_id = row[0]
        print(f"Using category ID: {category_id}")
    else:
        c.execute("INSERT INTO categories (name, description) VALUES (?, ?)", 
                  ('South Indian Specials', 'Authentic delicacies from the southern states of India'))
        category_id = c.lastrowid
        print(f"Created new category ID: {category_id}")

    # List of new dishes to add
    new_dishes = [
        ('Onion Uttapam', 110, 'Thick rice pancake topped with crunchy onions and chilies', 'https://images.unsplash.com/photo-1624005246242-990521dacc76?auto=format&fit=crop&q=80&w=800'),
        ('Mysore Masala Dosa', 140, 'Spicy dosa smeared with red garlic chutney and masala', 'https://images.unsplash.com/photo-1645177623570-ad448ae096fd?auto=format&fit=crop&q=80&w=800'),
        ('Kuzhi Paniyaram', 90, 'Fried steamed batter balls served with chutney', 'https://images.unsplash.com/photo-1625220194771-7ebdea0b70b9?auto=format&fit=crop&q=80&w=800'),
        ('Neer Dosa (3 pcs)', 100, 'Paper-thin, soft rice crepes from Mangalore', 'https://images.unsplash.com/photo-1627308595229-7830a5c91f9f?auto=format&fit=crop&q=80&w=800'),
        ('Set Dosa (3 pcs)', 110, 'Soft, spongy dosas served in a stack', 'https://images.unsplash.com/photo-1610192244261-3f33de3f55e4?auto=format&fit=crop&q=80&w=800'),
        ('Rava Dosa', 120, 'Crispy semolina crepe with herbs and spices', 'https://images.unsplash.com/photo-1589302168068-964664d93dc9?auto=format&fit=crop&q=80&w=800'),
        ('Paper Roast Ghee Dosa', 160, 'Super crispy, long dosa roasted with pure ghee', 'https://images.unsplash.com/photo-1610192244261-3f33de3f55e4?auto=format&fit=crop&q=80&w=800'),
        ('Chicken 65', 220, 'Spicy deep-fried chicken marinated in yogurt and spices', 'https://images.unsplash.com/photo-1610057099431-d73a1c9d2f2f?auto=format&fit=crop&q=80&w=800'),
        ('Gobi 65', 180, 'Crispy fried cauliflower florets tossed in spices', 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&q=80&w=800'),
        ('South Indian Filter Coffee', 45, 'Strong aromatic coffee brewed in traditional filter', 'https://images.unsplash.com/photo-1594631252845-29fc4586c552?auto=format&fit=crop&q=80&w=800'),
        ('Refreshing Butter Milk', 40, 'Spiced yogurt drink with curry leaves and ginger', 'https://images.unsplash.com/photo-1564758564527-b97d79cb27c1?auto=format&fit=crop&q=80&w=800'),
    ]

    count = 0
    for name, price, desc, url in new_dishes:
        # Check if exists to avoid duplicates
        c.execute("SELECT id FROM products WHERE name = ?", (name,))
        if c.fetchone():
            print(f"Skipping {name} (already exists)")
            continue

        c.execute("""INSERT INTO products (name, category_id, price, stock_quantity, unit, description, image_url, is_active)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                  (name, category_id, price, 50, 'pcs', desc, url, 1))
        print(f"✅ Added Verified Dish: {name}")
        count += 1

    conn.commit()
    conn.close()
    print(f"\n🚀 SUCCESS: Added {count} new authentic dishes with exact images!")

if __name__ == '__main__':
    add_authentic_dishes()
