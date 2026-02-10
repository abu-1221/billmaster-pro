from flask import Blueprint, request, jsonify
from backend.database import get_db

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/customers', methods=['GET', 'POST'])
def customers():
    action = request.args.get('action')
    conn = get_db()

    if action == 'list':
        custs = conn.execute("SELECT * FROM customers ORDER BY name").fetchall()
        conn.close()
        return jsonify({
            'success': True,
            'data': [dict(c) for c in custs]
        })

    elif action == 'create':
        data = request.get_json()
        conn.execute(
            "INSERT INTO customers (name, phone, email, address) VALUES (?, ?, ?, ?)",
            (data.get('name', ''), data.get('phone', ''), data.get('email', ''), data.get('address', ''))
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True})

    elif action == 'update':
        data = request.get_json()
        conn.execute(
            "UPDATE customers SET name=?, phone=?, email=?, address=? WHERE id=?",
            (data.get('name', ''), data.get('phone', ''), data.get('email', ''),
             data.get('address', ''), data.get('id'))
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True})

    elif action == 'delete':
        conn.execute("DELETE FROM customers WHERE id = ?", (request.args.get('id'),))
        conn.commit()
        conn.close()
        return jsonify({'success': True})

    conn.close()
    return jsonify({'success': False, 'message': 'Unknown action'})
