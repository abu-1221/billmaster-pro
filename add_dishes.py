"""
Add South Indian Dishes to BillMaster Pro Database
"""
import sqlite3
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'billmaster.db')

def add_dishes():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Check if Category exists, if not add it
    c.execute("SELECT id FROM categories WHERE name = 'South Indian'")
    row = c.fetchone()
    if row:
        category_id = row[0]
        print(f"Category 'South Indian' already exists (ID: {category_id})")
    else:
        c.execute("INSERT INTO categories (name, description) VALUES (?, ?)", 
                  ('South Indian', 'Authentic South Indian breakfast and meals'))
        category_id = c.lastrowid
        print(f"Added 'South Indian' category (ID: {category_id})")

    # 2. Add 15 Dishes with Unsplash URLs
    dishes = [
        ('Masala Dosa', 120, 'Crispy rice crepe filled with spiced potato masala', 
         'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&q=80&w=800'),
        ('Idli Sambhar (2 pcs)', 60, 'Soft steamed rice cakes served with lentil stew', 
         'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&q=80&w=800'),
        ('Medu Vada (2 pcs)', 80, 'Crispy deep-fried lentil donuts', 
         'https://images.unsplash.com/photo-1630383249896-424e482df921?auto=format&fit=crop&q=80&w=800'),
        ('Uttapam', 100, 'Thick rice pancake topped with onions and chillies', 
         'https://images.unsplash.com/photo-1624005246242-990521dacc76?auto=format&fit=crop&q=80&w=800'),
        ('Mysore Masala Dosa', 140, 'Crispy dosa with spicy garlic chutney and potato filling', 
         'https://images.unsplash.com/photo-1610192244261-3f33de3f55e4?auto=format&fit=crop&q=80&w=800'),
        ('Appam with Stew', 180, 'Lacy rice crepes served with creamy vegetable coconut stew', 
         'https://images.unsplash.com/photo-1626132646529-5006375040f1?auto=format&fit=crop&q=80&w=800'),
        ('Paniyaram (6 pcs)', 90, 'Small steamed and fried dumplings made of rice batter', 
         'https://images.unsplash.com/photo-1630409351241-e90e7f5e434d?auto=format&fit=crop&q=80&w=800'),
        ('Pongal', 70, 'Savory rice and lentil porridge tempered with pepper and ghee', 
         'https://images.unsplash.com/photo-1516714435131-44d6b64dc3a2?auto=format&fit=crop&q=80&w=800'),
        ('Rava Dosa', 110, 'Lacy, crispy dosa made of semolina and rice flour', 
         'https://images.unsplash.com/photo-1610192244261-3f33de3f55e4?auto=format&fit=crop&q=80&w=800'),
        ('Lemon Rice', 90, 'Zesty rice mixed with lemon juice, peanuts, and curry leaves', 
         'https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&q=80&w=800'),
        ('Curd Rice', 80, 'Soothing rice mixed with yogurt and tempered with mustard seeds', 
         'https://images.unsplash.com/photo-1546833359-0f666b6e4315?auto=format&fit=crop&q=80&w=800'),
        ('Paper Roast Dosa', 150, 'Extra large, super crispy paper-thin rice crepe', 
         'https://images.unsplash.com/photo-1630383249896-424e482df921?auto=format&fit=crop&q=80&w=800'),
        ('Kerala Paratha (2 pcs)', 100, 'Multi-layered flaky bread made with maida', 
         'https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&q=80&w=800'),
        ('Hyderabadi Biryani', 250, 'Fragrant basmati rice cooked with spices and vegetables', 
         'https://images.unsplash.com/photo-1563379091339-03b21bc4a6f8?auto=format&fit=crop&q=80&w=800'),
        ('Filter Coffee', 40, 'Traditional strong aromatic filter coffee with milk', 
         'https://images.unsplash.com/photo-1594631252845-29fc4586c552?auto=format&fit=crop&q=80&w=800'),
    ]

    for name, price, desc, url in dishes:
        # Check if product already exists
        c.execute("SELECT id FROM products WHERE name = ?", (name,))
        if c.fetchone():
            print(f"Dish '{name}' already exists, skipping.")
            continue
            
        c.execute("""INSERT INTO products (name, category_id, price, stock_quantity, unit, description, image_url, is_active)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                  (name, category_id, price, 100, 'pcs', desc, url, 1))
        print(f"Added dish: {name}")

    conn.commit()
    conn.close()
    print("\nSuccessfully added 15 South Indian dishes with images!")

if __name__ == '__main__':
    add_dishes()
