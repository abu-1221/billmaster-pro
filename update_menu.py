"""
Perfect South Indian Menu with Exact Images
"""
import sqlite3
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'billmaster.db')

def update_menu():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Get or Create Category
    c.execute("SELECT id FROM categories WHERE name = 'South Indian'")
    row = c.fetchone()
    if row:
        cat_id = row[0]
    else:
        c.execute("INSERT INTO categories (name, description) VALUES (?, ?)", 
                  ('South Indian', 'Authentic culinary delights from Southern India'))
        cat_id = c.lastrowid

    # 2. Clear old South Indian products to ensure "exact" images and no duplicates
    c.execute("DELETE FROM products WHERE category_id = ?", (cat_id,))

    # 3. 16 Perfect Dishes with unique, exact Unsplash images
    dishes = [
        ('Masala Dosa', 120, 'Crispy rice crepe with spiced potato filling', 
         'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&q=80&w=600'),
        ('Idli Sambhar', 60, 'Soft steamed rice cakes served with spicy sambar', 
         'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&q=80&w=600'),
        ('Medu Vada', 80, 'Savory deep-fried lentil donuts with chutney', 
         'https://images.unsplash.com/photo-1630383249896-424e482df921?auto=format&fit=crop&q=80&w=600'),
        ('Onion Uttapam', 100, 'Thick savory pancake topped with fresh onions', 
         'https://images.unsplash.com/photo-1624005246242-990521dacc76?auto=format&fit=crop&q=80&w=600'),
        ('Mysore Masala Dosa', 140, 'Spicy red chutney spread inside a crispy dosa', 
         'https://images.unsplash.com/photo-1645177623570-ad448ae096fd?auto=format&fit=crop&q=80&w=600'),
        ('Appam with Stew', 180, 'Lacy fermented rice crepes with vegetable stew', 
         'https://images.unsplash.com/photo-1626132646529-5006375040f1?auto=format&fit=crop&q=80&w=600'),
        ('Kuzhi Paniyaram', 90, 'Spiced rice batter dumplings roasted in a mold', 
         'https://images.unsplash.com/photo-1630409351241-e90e7f5e434d?auto=format&fit=crop&q=80&w=600'),
        ('Ven Pongal', 70, 'Ghee-tempered rice and lentil comfort food', 
         'https://images.unsplash.com/photo-1626509653295-3ca449419b4a?auto=format&fit=crop&q=80&w=600'),
        ('Rava Dosa', 110, 'Instant crispy dosa made from semolina', 
         'https://images.unsplash.com/photo-1610192244261-3f33de3f55e4?auto=format&fit=crop&q=80&w=600'),
        ('Lemon Rice', 90, 'Tangy turmeric rice with peanuts and curry leaves', 
         'https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&q=80&w=600'),
        ('Curd Rice', 80, 'Classic South Indian yogurt rice tempered with mustard', 
         'https://images.unsplash.com/photo-1588675646184-f5b0b0b0b2de?auto=format&fit=crop&q=80&w=600'),
        ('Paper Roast Dosa', 150, 'Ultra-thin long crispy golden dosa', 
         'https://images.unsplash.com/photo-1627308595229-7830a5c91f9f?auto=format&fit=crop&q=80&w=600'),
        ('Kerala Parotta', 100, 'Hand-tossed flaky multi-layered flatbread', 
         'https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&q=80&w=600'),
        ('Vegetable Biryani', 220, 'Aromatic basmati rice cooked with fresh veggies', 
         'https://images.unsplash.com/photo-1563379091339-03b21bc4a6f8?auto=format&fit=crop&q=80&w=600'),
        ('Filter Coffee', 40, 'Traditional strongly brewed chicory-coffee blend', 
         'https://images.unsplash.com/photo-1594631252845-29fc4586c552?auto=format&fit=crop&q=80&w=600'),
        ('Chicken 65', 250, 'Spicy, deep-fried chicken tempered with curry leaves', 
         'https://images.unsplash.com/photo-1610057099431-d73a1c9d2f2f?auto=format&fit=crop&q=80&w=600'),
    ]

    for name, price, desc, url in dishes:
        c.execute("""INSERT INTO products (name, category_id, price, stock_quantity, unit, description, image_url, is_active)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                  (name, cat_id, price, 100, 'pcs', desc, url, 1))
        print(f"Created: {name}")

    conn.commit()
    conn.close()
    print("\n✅ Perfect menu with 16 dishes and exact images updated!")

if __name__ == '__main__':
    update_menu()
