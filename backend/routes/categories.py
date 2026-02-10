from flask import Blueprint, request, jsonify
from backend.database import get_db

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories', methods=['GET', 'POST'])
def categories():
    action = request.args.get('action')
    conn = get_db()

    if action == 'list':
        cats = conn.execute("""
            SELECT c.*, COUNT(p.id) as product_count 
            FROM categories c 
            LEFT JOIN products p ON p.category_id = c.id 
            GROUP BY c.id
            ORDER BY c.name
        """).fetchall()
        conn.close()
        return jsonify({
            'success': True,
            'data': [dict(c) for c in cats]
        })

    elif action == 'create':
        data = request.get_json()
        conn.execute(
            "INSERT INTO categories (name, description) VALUES (?, ?)",
            (data.get('name', ''), data.get('description', ''))
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True})

    elif action == 'update':
        data = request.get_json()
        conn.execute(
            "UPDATE categories SET name = ?, description = ? WHERE id = ?",
            (data.get('name', ''), data.get('description', ''), data.get('id'))
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True})

    elif action == 'delete':
        cat_id = request.args.get('id')
        count = conn.execute(
            "SELECT COUNT(*) FROM products WHERE category_id = ?", (cat_id,)
        ).fetchone()[0]

        if count > 0:
            conn.close()
            return jsonify({'success': False, 'message': 'Cannot delete: category has products'})

        conn.execute("DELETE FROM categories WHERE id = ?", (cat_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})

    conn.close()
    return jsonify({'success': False, 'message': 'Unknown action'})
