from flask import Blueprint, request, jsonify
from backend.database import get_db

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET', 'POST'])
def products():
    action = request.args.get('action')
    conn = get_db()

    if action == 'list':
        active_only = request.args.get('active_only')
        query = """
            SELECT p.*, COALESCE(c.name, 'None') as category_name 
            FROM products p 
            LEFT JOIN categories c ON p.category_id = c.id
        """
        if active_only:
            query += " WHERE p.is_active = 1"
        query += " ORDER BY p.name"

        prods = conn.execute(query).fetchall()
        conn.close()
        return jsonify({
            'success': True,
            'data': [dict(p) for p in prods]
        })

    elif action == 'create':
        data = request.get_json()
        conn.execute(
            """INSERT INTO products (name, category_id, price, stock_quantity, unit, description, image_url, is_active) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                data.get('name', ''),
                data.get('category_id'),
                float(data.get('price', 0)),
                int(data.get('stock_quantity', 0)),
                data.get('unit', 'pcs'),
                data.get('description', ''),
                data.get('image_url', ''),
                int(data.get('is_active', 1))
            )
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True})

    elif action == 'update':
        data = request.get_json()
        conn.execute(
            """UPDATE products SET name=?, category_id=?, price=?, stock_quantity=?, 
               unit=?, description=?, image_url=?, is_active=? WHERE id=?""",
            (
                data.get('name', ''),
                data.get('category_id'),
                float(data.get('price', 0)),
                int(data.get('stock_quantity', 0)),
                data.get('unit', 'pcs'),
                data.get('description', ''),
                data.get('image_url', ''),
                int(data.get('is_active', 1)),
                data.get('id')
            )
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True})

    elif action == 'delete':
        conn.execute("DELETE FROM products WHERE id = ?", (request.args.get('id'),))
        conn.commit()
        conn.close()
        return jsonify({'success': True})

    conn.close()
    return jsonify({'success': False, 'message': 'Unknown action'})
