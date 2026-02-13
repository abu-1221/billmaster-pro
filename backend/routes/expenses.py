from flask import Blueprint, request, jsonify, session
from backend.database import get_db

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/expenses', methods=['GET', 'POST'])
def expenses():
    # ONLY ADMINS CAN ACCESS EXPENSES
    if session.get('role') != 'admin':
        return jsonify({'success': False, 'message': 'Access denied: Requires Admin role'})

    action = request.args.get('action')
    conn = get_db()

    if action == 'list':
        rows = conn.execute("SELECT * FROM expenses ORDER BY expense_date DESC").fetchall()
        conn.close()
        return jsonify({'success': True, 'data': [dict(r) for r in rows]})

    elif action == 'add':
        data = request.get_json()
        title = data.get('title')
        amount = data.get('amount', 0)
        category = data.get('category', 'general')
        expense_date = data.get('expense_date')
        description = data.get('description', '')

        if not title or not amount:
            conn.close()
            return jsonify({'success': False, 'message': 'Title and amount are required'})

        conn.execute(
            "INSERT INTO expenses (title, amount, category, expense_date, description) VALUES (?, ?, ?, ?, ?)",
            (title, amount, category, expense_date, description)
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Expense added successfully'})

    elif action == 'delete':
        expense_id = request.args.get('id')
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})

    conn.close()
    return jsonify({'success': False, 'message': 'Unknown action'})
