from flask import Blueprint, request, jsonify
from backend.database import get_db
from datetime import datetime

invoices_bp = Blueprint('invoices', __name__)

@invoices_bp.route('/invoices', methods=['GET', 'POST'])
def invoices():
    action = request.args.get('action')
    conn = get_db()

    if action == 'list':
        invs = conn.execute("SELECT * FROM invoices ORDER BY created_at DESC").fetchall()
        result = []
        for inv in invs:
            inv_dict = dict(inv)
            items = conn.execute(
                "SELECT * FROM invoice_items WHERE invoice_id = ?", (inv['id'],)
            ).fetchall()
            inv_dict['items'] = [dict(item) for item in items]
            result.append(inv_dict)
        conn.close()
        return jsonify({'success': True, 'data': result})

    elif action == 'get':
        inv_id = request.args.get('id')
        inv = conn.execute("SELECT * FROM invoices WHERE id = ?", (inv_id,)).fetchone()
        if not inv:
            conn.close()
            return jsonify({'success': False, 'message': 'Invoice not found'})

        inv_dict = dict(inv)
        items = conn.execute(
            "SELECT * FROM invoice_items WHERE invoice_id = ?", (inv_id,)
        ).fetchall()
        inv_dict['items'] = [dict(item) for item in items]
        conn.close()
        return jsonify({'success': True, 'data': inv_dict})

    elif action == 'create':
        data = request.get_json()

        prefix_row = conn.execute(
            "SELECT value FROM settings WHERE key = 'invoice_prefix'"
        ).fetchone()
        prefix = prefix_row['value'] if prefix_row else 'INV'

        last = conn.execute("SELECT MAX(id) as max_id FROM invoices").fetchone()
        next_id = (last['max_id'] or 0) + 1
        inv_number = f"{prefix}-{next_id:05d}"

        customer_name = None
        if data.get('customer_id'):
            cust = conn.execute(
                "SELECT name FROM customers WHERE id = ?", (data['customer_id'],)
            ).fetchone()
            customer_name = cust['name'] if cust else None

        cursor = conn.execute(
            """INSERT INTO invoices 
               (invoice_number, customer_id, customer_name, subtotal, total_amount, 
                payment_method, payment_status, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                inv_number,
                data.get('customer_id'),
                customer_name,
                float(data.get('subtotal', 0)),
                float(data.get('total_amount', 0)),
                data.get('payment_method', 'cash'),
                data.get('payment_status', 'paid'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        )
        invoice_id = cursor.lastrowid

        for item in data.get('items', []):
            product = conn.execute(
                "SELECT name FROM products WHERE id = ?", (item['product_id'],)
            ).fetchone()
            product_name = product['name'] if product else 'Unknown'

            conn.execute(
                """INSERT INTO invoice_items 
                   (invoice_id, product_id, product_name, quantity, unit_price, total_price)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    invoice_id,
                    item['product_id'],
                    product_name,
                    int(item['quantity']),
                    float(item['unit_price']),
                    float(item['unit_price']) * int(item['quantity'])
                )
            )

            conn.execute(
                "UPDATE products SET stock_quantity = MAX(0, stock_quantity - ?) WHERE id = ?",
                (int(item['quantity']), item['product_id'])
            )

        if data.get('customer_id'):
            conn.execute(
                """UPDATE customers SET 
                   total_orders = total_orders + 1,
                   total_spent = total_spent + ?
                   WHERE id = ?""",
                (float(data.get('total_amount', 0)), data['customer_id'])
            )

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'invoice_id': invoice_id})

    conn.close()
    return jsonify({'success': False, 'message': 'Unknown action'})
