from flask import Blueprint, request, jsonify, session
from backend.database import get_db

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    action = request.args.get('action')
    conn = get_db()

    if action == 'get':
        rows = conn.execute("SELECT * FROM settings").fetchall()
        data = {r['key']: r['value'] for r in rows}
        conn.close()
        return jsonify({'success': True, 'data': data})

    elif action == 'update':
        data = request.get_json()
        for key, value in data.items():
            conn.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                (key, str(value))
            )
        conn.commit()
        conn.close()
        return jsonify({'success': True})

    elif action == 'users':
        # ONLY ADMINS CAN LIST USERS
        if session.get('role') != 'admin':
            conn.close()
            return jsonify({'success': False, 'message': 'Access denied'})

        users = conn.execute(
            "SELECT id, username, full_name, role, created_at FROM users ORDER BY id"
        ).fetchall()
        conn.close()
        return jsonify({'success': True, 'data': [dict(u) for u in users]})

    elif action == 'delete_user':
        # ONLY ADMINS CAN DELETE USERS
        if session.get('role') != 'admin':
            conn.close()
            return jsonify({'success': False, 'message': 'Access denied'})

        user_id = request.args.get('id')
        # Prevent deleting the main admin (ID 1)
        if str(user_id) == '1':
            conn.close()
            return jsonify({'success': False, 'message': 'Cannot delete the primary administrator'})

        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})

    elif action == 'factory_reset':
        # ONLY ADMINS CAN RESET DATABASE
        if session.get('role') != 'admin':
            conn.close()
            return jsonify({'success': False, 'message': 'Access denied'})

        # WIPE ALL DATA EXCEPT USERS
        conn.execute("DELETE FROM invoice_items")
        conn.execute("DELETE FROM invoices")
        conn.execute("DELETE FROM products")
        conn.execute("DELETE FROM customers")
        conn.execute("DELETE FROM categories")
        # Reset auto-increments
        conn.execute("DELETE FROM sqlite_sequence WHERE name IN ('invoices', 'products', 'customers', 'categories')")
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'System reset successfully'})

    conn.close()
    return jsonify({'success': False, 'message': 'Unknown action'})
