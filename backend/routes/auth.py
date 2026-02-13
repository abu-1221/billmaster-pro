from flask import Blueprint, request, jsonify, session
from backend.database import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth', methods=['GET', 'POST'])
def auth():
    action = request.args.get('action')

    if action == 'check':
        if 'user_id' in session:
            return jsonify({
                'success': True,
                'user': {
                    'id': session['user_id'],
                    'username': session['username'],
                    'full_name': session['full_name'],
                    'role': session['role']
                }
            })
        return jsonify({'success': False})

    elif action == 'login':
        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            session['role'] = user['role']
            return jsonify({
                'success': True,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'full_name': user['full_name'],
                    'role': user['role']
                }
            })
        return jsonify({'success': False, 'message': 'Invalid username or password'})

    elif action == 'logout':
        session.clear()
        return jsonify({'success': True})

    elif action == 'register':
        # ONLY ADMINS CAN REGISTER NEW USERS
        if session.get('role') != 'admin':
            return jsonify({'success': False, 'message': 'Access denied: Requires Admin role'})

        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')
        full_name = data.get('full_name', '')
        role = data.get('role', 'staff')

        conn = get_db()
        existing = conn.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()

        if existing:
            conn.close()
            return jsonify({'success': False, 'message': 'Username already exists'})

        conn.execute(
            "INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
            (username, password, full_name, role)
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'User {username} created successfully as {role}'})

    elif action == 'update_password':
        # ONLY ADMINS CAN UPDATE OTHER USERS' PASSWORDS
        if session.get('role') != 'admin':
            return jsonify({'success': False, 'message': 'Access denied: Requires Admin role'})

        data = request.get_json()
        user_id = data.get('id')
        new_password = data.get('password')

        if not user_id or not new_password:
            return jsonify({'success': False, 'message': 'Missing user ID or password'})

        conn = get_db()
        conn.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (new_password, user_id)
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Password updated successfully'})

    return jsonify({'success': False, 'message': 'Unknown action'})
