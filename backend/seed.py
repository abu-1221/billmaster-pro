"""
BillMaster Pro - Database Seed Data
Populates the database with sample data for development & demo.
"""

import random
from datetime import datetime, timedelta


def seed_database(db):
    """Populate database with sample data."""
    if db.is_seeded():
        return False

    conn = db.get_connection()
    cursor = conn.cursor()

    # ── Users ────────────────────────────────────────
    users = [
        ('admin', 'admin123', 'Admin User', 'admin'),
        ('staff', 'staff123', 'Staff Member', 'staff'),
        ('cashier1', 'cashier123', 'Ramesh Kumar', 'staff'),
        ('cashier2', 'cashier123', 'Sunita Devi', 'staff'),
        ('manager', 'manager123', 'Vijay Sharma', 'admin'),
    ]
    cursor.executemany(
        "INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
        users
    )

    # ── Categories ───────────────────────────────────
    categories = [
        ('Groceries', 'Daily grocery items and essentials'),
        ('Beverages', 'Drinks, juices, and soft drinks'),
        ('Snacks', 'Chips, biscuits, and packaged snacks'),
        ('Dairy', 'Milk, cheese, butter, and dairy products'),
        ('Personal Care', 'Soaps, shampoos, and hygiene products'),
        ('Stationery', 'Pens, notebooks, and office supplies'),
        ('Electronics', 'Mobile accessories, chargers, and gadgets'),
        ('Frozen Foods', 'Frozen snacks, ice cream, and ready-to-eat meals'),
        ('Cleaning Supplies', 'Detergents, floor cleaners, and disinfectants'),
        ('Baby Products', 'Diapers, baby food, and baby care items'),
        ('Spices & Masala', 'Indian spices, masala powders, and seasonings'),
    ]
    cursor.executemany(
        "INSERT INTO categories (name, description) VALUES (?, ?)",
        categories
    )

    # Build category map
    cursor.execute("SELECT id, name FROM categories")
    cat = {row[1]: row[0] for row in cursor.fetchall()}

    # ── Products ─────────────────────────────────────
    products = [
        # Groceries
        ('Basmati Rice (5kg)', cat['Groceries'], 450, 50, 'pcs', 'Premium long grain basmati rice'),
        ('Toor Dal (1kg)', cat['Groceries'], 160, 80, 'pcs', 'Yellow split lentils'),
        ('Sunflower Oil (1L)', cat['Groceries'], 180, 40, 'pcs', 'Refined sunflower cooking oil'),
        ('Sugar (1kg)', cat['Groceries'], 50, 100, 'kg', 'White sugar'),
        ('Wheat Flour (5kg)', cat['Groceries'], 280, 35, 'pcs', 'Chakki fresh atta'),
        ('Maggi Noodles (12 pack)', cat['Groceries'], 168, 90, 'pcs', 'Instant masala noodles'),
        ('Aashirvaad Atta (10kg)', cat['Groceries'], 520, 25, 'pcs', 'Whole wheat flour'),
        ('Fortune Mustard Oil (1L)', cat['Groceries'], 210, 35, 'pcs', 'Pure mustard oil'),
        ('Tata Salt (1kg)', cat['Groceries'], 28, 120, 'pcs', 'Iodized table salt'),
        ('Saffola Gold Oil (1L)', cat['Groceries'], 250, 30, 'pcs', 'Healthy cooking oil'),
        ('Rajma (1kg)', cat['Groceries'], 140, 50, 'pcs', 'Red kidney beans'),
        ('Chana Dal (1kg)', cat['Groceries'], 120, 55, 'pcs', 'Bengal gram split'),
        ('Poha (500g)', cat['Groceries'], 40, 70, 'pcs', 'Flattened rice flakes'),

        # Beverages
        ('Coca Cola (500ml)', cat['Beverages'], 40, 120, 'pcs', 'Carbonated soft drink'),
        ('Pepsi (500ml)', cat['Beverages'], 40, 100, 'pcs', 'Carbonated soft drink'),
        ('Mango Juice (1L)', cat['Beverages'], 90, 60, 'pcs', 'Real mango fruit juice'),
        ('Green Tea (25 bags)', cat['Beverages'], 150, 45, 'pcs', 'Organic green tea bags'),
        ('Mineral Water (1L)', cat['Beverages'], 20, 200, 'pcs', 'Packaged drinking water'),
        ('Thumbs Up (750ml)', cat['Beverages'], 45, 80, 'pcs', 'Cola soft drink'),
        ('Sprite (500ml)', cat['Beverages'], 40, 90, 'pcs', 'Lemon lime soft drink'),
        ('Red Bull Energy (250ml)', cat['Beverages'], 125, 40, 'pcs', 'Energy drink'),
        ('Tropicana Orange (1L)', cat['Beverages'], 110, 35, 'pcs', 'Orange fruit juice'),
        ('Bisleri Water (2L)', cat['Beverages'], 30, 150, 'pcs', 'Packaged drinking water'),
        ('Nescafe Coffee (50g)', cat['Beverages'], 175, 45, 'pcs', 'Instant coffee powder'),
        ('Tata Tea Gold (500g)', cat['Beverages'], 260, 40, 'pcs', 'Premium leaf tea'),

        # Snacks
        ('Lays Classic (150g)', cat['Snacks'], 60, 75, 'pcs', 'Classic salted potato chips'),
        ('Oreo Biscuits', cat['Snacks'], 35, 90, 'pcs', 'Chocolate cream biscuits'),
        ('Mixed Nuts (250g)', cat['Snacks'], 320, 25, 'pcs', 'Premium assorted dry fruits'),
        ('Kurkure (100g)', cat['Snacks'], 30, 110, 'pcs', 'Masala crunch snack'),
        ('Haldiram Namkeen (200g)', cat['Snacks'], 80, 65, 'pcs', 'Aloo bhujia mixture'),
        ('Dark Fantasy Biscuit', cat['Snacks'], 45, 80, 'pcs', 'Choco filled cookies'),
        ('Cadbury Dairy Milk (110g)', cat['Snacks'], 100, 70, 'pcs', 'Milk chocolate bar'),
        ('5 Star Chocolate', cat['Snacks'], 20, 120, 'pcs', 'Caramel nougat bar'),
        ('Pringles Original (107g)', cat['Snacks'], 199, 30, 'pcs', 'Stackable potato crisps'),
        ('Bingo Mad Angles', cat['Snacks'], 20, 100, 'pcs', 'Achaari masti snack'),

        # Dairy
        ('Amul Milk (500ml)', cat['Dairy'], 30, 150, 'pcs', 'Full cream toned milk'),
        ('Cheddar Cheese (200g)', cat['Dairy'], 180, 30, 'pcs', 'Processed cheddar cheese slices'),
        ('Amul Butter (200g)', cat['Dairy'], 110, 40, 'pcs', 'Pasteurized salted butter'),
        ('Yoghurt (400g)', cat['Dairy'], 45, 60, 'pcs', 'Fresh set yoghurt'),
        ('Paneer (200g)', cat['Dairy'], 90, 40, 'pcs', 'Fresh cottage cheese'),
        ('Amul Lassi (200ml)', cat['Dairy'], 25, 80, 'pcs', 'Sweet mango lassi'),
        ('Cream (200ml)', cat['Dairy'], 65, 35, 'pcs', 'Fresh dairy cream'),
        ('Milkmaid (400g)', cat['Dairy'], 155, 30, 'pcs', 'Sweetened condensed milk'),

        # Personal Care
        ('Dove Soap (100g)', cat['Personal Care'], 65, 80, 'pcs', 'Moisturizing beauty bar'),
        ('Head & Shoulders (200ml)', cat['Personal Care'], 230, 35, 'pcs', 'Anti-dandruff shampoo'),
        ('Colgate Toothpaste (150g)', cat['Personal Care'], 85, 55, 'pcs', 'Cavity protection toothpaste'),
        ('Dettol Handwash (250ml)', cat['Personal Care'], 95, 50, 'pcs', 'Antibacterial hand wash'),
        ('Nivea Body Lotion (200ml)', cat['Personal Care'], 199, 30, 'pcs', 'Moisturizing body lotion'),
        ('Gillette Razor (Pack of 5)', cat['Personal Care'], 120, 40, 'pcs', 'Disposable shaving razors'),
        ('Lux Soap (3 pack)', cat['Personal Care'], 135, 55, 'pcs', 'Fragrant beauty soap'),
        ('Vaseline (100ml)', cat['Personal Care'], 95, 45, 'pcs', 'Petroleum jelly'),

        # Stationery
        ('Notebook (200 pages)', cat['Stationery'], 60, 100, 'pcs', 'Ruled long notebook'),
        ('Ball Pen (Pack of 10)', cat['Stationery'], 50, 70, 'pcs', 'Blue ink ball pens'),
        ('A4 Paper (500 sheets)', cat['Stationery'], 350, 20, 'pcs', 'White A4 printing paper'),
        ('Marker Set (8 colors)', cat['Stationery'], 120, 40, 'pcs', 'Permanent color markers'),
        ('Stapler with Pins', cat['Stationery'], 85, 30, 'pcs', 'Desktop stapler set'),
        ('Scissors', cat['Stationery'], 45, 50, 'pcs', 'Stainless steel scissors'),
        ('Glue Stick (Pack of 3)', cat['Stationery'], 60, 65, 'pcs', 'Non-toxic glue sticks'),
        ('Sticky Notes (100 sheets)', cat['Stationery'], 50, 80, 'pcs', 'Colorful sticky note pads'),

        # Electronics
        ('iPhone Charger Cable', cat['Electronics'], 299, 40, 'pcs', 'Lightning to USB-C cable'),
        ('Wireless Earbuds', cat['Electronics'], 1499, 25, 'pcs', 'Bluetooth 5.0 TWS earbuds'),
        ('Power Bank 10000mAh', cat['Electronics'], 899, 30, 'pcs', 'Fast charging portable charger'),
        ('USB-C Hub 4-in-1', cat['Electronics'], 650, 20, 'pcs', 'Multi-port USB hub adapter'),
        ('Phone Screen Guard', cat['Electronics'], 149, 100, 'pcs', 'Tempered glass protector'),
        ('LED Desk Lamp', cat['Electronics'], 599, 15, 'pcs', 'Rechargeable study lamp'),
        ('Bluetooth Speaker', cat['Electronics'], 1299, 18, 'pcs', 'Portable waterproof speaker'),
        ('Mouse Wireless', cat['Electronics'], 399, 35, 'pcs', 'Ergonomic wireless mouse'),

        # Frozen Foods
        ('Frozen Samosa (12pcs)', cat['Frozen Foods'], 120, 50, 'pcs', 'Ready to fry samosas'),
        ('Ice Cream Vanilla (1L)', cat['Frozen Foods'], 199, 30, 'pcs', 'Amul vanilla ice cream'),
        ('Frozen Pizza (Medium)', cat['Frozen Foods'], 250, 25, 'pcs', 'Cheese burst frozen pizza'),
        ('Frozen Momos (20pcs)', cat['Frozen Foods'], 150, 40, 'pcs', 'Chicken momos ready to steam'),
        ('Frozen French Fries (500g)', cat['Frozen Foods'], 130, 45, 'pcs', 'Crispy french fries'),
        ('Ice Cream Chocolate (1L)', cat['Frozen Foods'], 220, 28, 'pcs', 'Rich chocolate ice cream'),

        # Cleaning Supplies
        ('Surf Excel (1kg)', cat['Cleaning Supplies'], 195, 60, 'pcs', 'Washing powder detergent'),
        ('Lizol Floor Cleaner (1L)', cat['Cleaning Supplies'], 175, 45, 'pcs', 'Citrus floor disinfectant'),
        ('Vim Dishwash Gel (500ml)', cat['Cleaning Supplies'], 110, 55, 'pcs', 'Lemon dishwashing liquid'),
        ('Harpic Toilet Cleaner', cat['Cleaning Supplies'], 95, 50, 'pcs', 'Powerful toilet cleaner'),
        ('Colin Glass Cleaner', cat['Cleaning Supplies'], 85, 35, 'pcs', 'Streak-free glass cleaner'),
        ('Scotch Brite Scrub Pad', cat['Cleaning Supplies'], 30, 100, 'pcs', 'Heavy duty scrub pad'),
        ('Room Freshener (300ml)', cat['Cleaning Supplies'], 199, 30, 'pcs', 'Odonil room freshener spray'),

        # Baby Products
        ('Pampers Diapers (M, 20pcs)', cat['Baby Products'], 450, 40, 'pcs', 'Medium size baby diapers'),
        ('Cerelac Baby Food (300g)', cat['Baby Products'], 280, 35, 'pcs', 'Wheat apple baby cereal'),
        ('Johnson Baby Soap', cat['Baby Products'], 75, 60, 'pcs', 'Gentle baby bath soap'),
        ('Baby Wipes (72pcs)', cat['Baby Products'], 150, 50, 'pcs', 'Gentle cleansing wipes'),
        ('Johnson Baby Oil (200ml)', cat['Baby Products'], 180, 30, 'pcs', 'Moisturizing baby oil'),
        ('Baby Powder (200g)', cat['Baby Products'], 120, 45, 'pcs', 'Talcum powder for babies'),

        # Spices & Masala
        ('Turmeric Powder (200g)', cat['Spices & Masala'], 55, 80, 'pcs', 'Pure haldi powder'),
        ('Red Chilli Powder (200g)', cat['Spices & Masala'], 65, 70, 'pcs', 'Kashmiri mirch powder'),
        ('Garam Masala (100g)', cat['Spices & Masala'], 75, 60, 'pcs', 'MDH garam masala blend'),
        ('Coriander Powder (200g)', cat['Spices & Masala'], 45, 75, 'pcs', 'Dhaniya powder'),
        ('Cumin Seeds (100g)', cat['Spices & Masala'], 60, 65, 'pcs', 'Whole jeera seeds'),
        ('Black Pepper (100g)', cat['Spices & Masala'], 120, 40, 'pcs', 'Whole black peppercorns'),
        ('Biryani Masala (50g)', cat['Spices & Masala'], 55, 50, 'pcs', 'Special biryani spice mix'),
        ('Kitchen King Masala (100g)', cat['Spices & Masala'], 70, 55, 'pcs', 'All-purpose cooking masala'),
    ]
    cursor.executemany(
        "INSERT INTO products (name, category_id, price, stock_quantity, unit, description) VALUES (?, ?, ?, ?, ?, ?)",
        products
    )

    # ── Customers ────────────────────────────────────
    customers = [
        ('Rahul Sharma', '9876543210', 'rahul@example.com', '12, MG Road, Mumbai', 15, 12500),
        ('Priya Patel', '9876543211', 'priya@example.com', '45, Park Street, Delhi', 8, 7800),
        ('Amit Kumar', '9876543212', 'amit@example.com', '78, Lake View, Bangalore', 22, 18900),
        ('Sneha Reddy', '9876543213', 'sneha@example.com', '23, Beach Road, Chennai', 5, 4200),
        ('Vikram Singh', '9876543214', 'vikram@example.com', '56, Civil Lines, Jaipur', 12, 9600),
        ('Arjun Mehta', '9871234501', 'arjun@example.com', '10, Sector 21, Noida', 0, 0),
        ('Deepika Joshi', '9871234502', 'deepika@example.com', '34, Jayanagar, Bangalore', 0, 0),
        ('Ravi Verma', '9871234503', 'ravi@example.com', '88, Banjara Hills, Hyderabad', 0, 0),
        ('Anjali Gupta', '9871234504', 'anjali@example.com', '5, Connaught Place, Delhi', 0, 0),
        ('Suresh Iyer', '9871234505', 'suresh@example.com', '67, Anna Nagar, Chennai', 0, 0),
        ('Kavita Deshmukh', '9871234506', 'kavita@example.com', '12, FC Road, Pune', 0, 0),
        ('Mohammed Farooq', '9871234507', 'farooq@example.com', '9, Charminar Road, Hyderabad', 0, 0),
        ('Nisha Agarwal', '9871234508', 'nisha@example.com', '45, Mall Road, Lucknow', 0, 0),
        ('Rajesh Nair', '9871234509', 'rajesh@example.com', '23, MG Road, Kochi', 0, 0),
        ('Pooja Saxena', '9871234510', 'pooja@example.com', '78, Hazratganj, Lucknow', 0, 0),
        ('Sanjay Tiwari', '9871234511', 'sanjay@example.com', '56, Civil Lines, Allahabad', 0, 0),
        ('Meera Krishnan', '9871234512', 'meera@example.com', '30, T Nagar, Chennai', 0, 0),
        ('Aditya Kapoor', '9871234513', 'aditya@example.com', '15, Sector 44, Gurgaon', 0, 0),
        ('Shreya Das', '9871234514', 'shreya@example.com', '8, Salt Lake, Kolkata', 0, 0),
        ('Karan Malhotra', '9871234515', 'karan@example.com', '42, Model Town, Jalandhar', 0, 0),
    ]
    cursor.executemany(
        "INSERT INTO customers (name, phone, email, address, total_orders, total_spent) VALUES (?, ?, ?, ?, ?, ?)",
        customers
    )

    # ── Settings ─────────────────────────────────────
    settings = [
        ('business_name', 'BillMaster Pro Store'),
        ('business_address', '123, Main Street, City Center'),
        ('business_phone', '+91 98765 43210'),
        ('business_email', 'store@billmaster.com'),
        ('currency_symbol', '\u20b9'),
        ('tax_rate', '0'),
        ('invoice_prefix', 'INV'),
    ]
    cursor.executemany(
        "INSERT INTO settings (key, value) VALUES (?, ?)",
        settings
    )

    # ── Sample Invoices (30 days of data) ────────────
    cursor.execute("SELECT id, name, price FROM products")
    all_products = cursor.fetchall()

    cursor.execute("SELECT id, name FROM customers")
    all_customers = cursor.fetchall()

    payment_methods = ['cash', 'card', 'upi', 'bank_transfer']
    now = datetime.now()
    invoice_count = 0

    for day in range(30, -1, -1):
        date = now - timedelta(days=day)
        invoices_per_day = random.randint(3, 8)

        for _ in range(invoices_per_day):
            invoice_count += 1
            inv_number = f"INV-{invoice_count:05d}"

            hour = random.randint(8, 21)
            minute = random.randint(0, 59)
            inv_date = date.replace(hour=hour, minute=minute, second=0, microsecond=0)

            customer = random.choice(all_customers) if random.random() > 0.35 else None
            customer_id = customer['id'] if customer else None
            customer_name = customer['name'] if customer else None

            num_items = random.randint(1, 5)
            chosen = random.sample(list(all_products), min(num_items, len(all_products)))

            subtotal = 0
            items_data = []
            for prod in chosen:
                qty = random.randint(1, 3)
                total_price = prod['price'] * qty
                subtotal += total_price
                items_data.append((prod['id'], prod['name'], qty, prod['price'], total_price))

            payment_method = random.choice(payment_methods)
            payment_status = 'paid' if random.random() > 0.12 else 'pending'

            cursor.execute(
                """INSERT INTO invoices 
                   (invoice_number, customer_id, customer_name, subtotal, total_amount,
                    payment_method, payment_status, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (inv_number, customer_id, customer_name, subtotal, subtotal,
                 payment_method, payment_status, inv_date.strftime('%Y-%m-%d %H:%M:%S'))
            )
            real_invoice_id = cursor.lastrowid

            for item in items_data:
                cursor.execute(
                    """INSERT INTO invoice_items 
                       (invoice_id, product_id, product_name, quantity, unit_price, total_price)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (real_invoice_id, item[0], item[1], item[2], item[3], item[4])
                )

    conn.commit()
    conn.close()
    return invoice_count
