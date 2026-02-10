from flask import Blueprint, request, jsonify
from backend.database import get_db
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics', methods=['GET'])
def analytics():
    action = request.args.get('action')
    conn = get_db()

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_str = today.strftime('%Y-%m-%d %H:%M:%S')
    yesterday = today - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d %H:%M:%S')

    if action == 'dashboard':
        today_row = conn.execute("""
            SELECT COALESCE(SUM(total_amount), 0) as revenue, COUNT(*) as invoices
            FROM invoices WHERE created_at >= ?
        """, (today_str,)).fetchone()

        today_items = conn.execute("""
            SELECT COALESCE(SUM(ii.quantity), 0) as items_sold
            FROM invoice_items ii
            JOIN invoices i ON ii.invoice_id = i.id
            WHERE i.created_at >= ?
        """, (today_str,)).fetchone()

        yesterday_row = conn.execute("""
            SELECT COALESCE(SUM(total_amount), 0) as revenue, COUNT(*) as invoices
            FROM invoices WHERE created_at >= ? AND created_at < ?
        """, (yesterday_str, today_str)).fetchone()

        month_start = today.replace(day=1).strftime('%Y-%m-%d %H:%M:%S')
        month_row = conn.execute("""
            SELECT COALESCE(SUM(total_amount), 0) as revenue
            FROM invoices WHERE created_at >= ?
        """, (month_start,)).fetchone()

        today_rev = today_row['revenue']
        yesterday_rev = yesterday_row['revenue']
        revenue_growth = round(((today_rev - yesterday_rev) / yesterday_rev) * 100) if yesterday_rev > 0 else 0

        conn.close()
        return jsonify({
            'success': True,
            'data': {
                'today': {
                    'revenue': today_rev,
                    'invoices': today_row['invoices'],
                    'items_sold': today_items['items_sold']
                },
                'yesterday': {
                    'invoices': yesterday_row['invoices']
                },
                'month': {
                    'revenue': month_row['revenue']
                },
                'revenue_growth': revenue_growth
            }
        })

    elif action == 'sales_chart':
        days = int(request.args.get('days', 14))
        data = []
        for i in range(days - 1, -1, -1):
            d = today - timedelta(days=i)
            next_d = d + timedelta(days=1)
            d_str = d.strftime('%Y-%m-%d %H:%M:%S')
            next_d_str = next_d.strftime('%Y-%m-%d %H:%M:%S')

            row = conn.execute("""
                SELECT COALESCE(SUM(total_amount), 0) as total,
                       COALESCE(SUM(CASE WHEN payment_status='paid' THEN total_amount ELSE 0 END), 0) as paid
                FROM invoices WHERE created_at >= ? AND created_at < ?
            """, (d_str, next_d_str)).fetchone()

            data.append({
                'date': d.strftime('%Y-%m-%d'),
                'total': row['total'],
                'paid': row['paid']
            })

        conn.close()
        return jsonify({'success': True, 'data': data})

    elif action == 'payment_methods':
        rows = conn.execute("""
            SELECT payment_method, SUM(total_amount) as total
            FROM invoices 
            GROUP BY payment_method
        """).fetchall()

        grand_total = sum(r['total'] for r in rows)
        data = [{
            'payment_method': r['payment_method'],
            'total': r['total'],
            'percentage': round((r['total'] / grand_total) * 100) if grand_total > 0 else 0
        } for r in rows]

        conn.close()
        return jsonify({'success': True, 'data': data})

    elif action == 'top_products':
        limit = int(request.args.get('limit', 5))
        rows = conn.execute("""
            SELECT ii.product_name as name,
                   SUM(ii.quantity) as sold,
                   SUM(ii.total_price) as revenue,
                   ROUND(SUM(ii.total_price) * 1.0 / SUM(ii.quantity), 2) as avg_price
            FROM invoice_items ii
            GROUP BY ii.product_id
            ORDER BY revenue DESC
            LIMIT ?
        """, (limit,)).fetchall()

        conn.close()
        return jsonify({'success': True, 'data': [dict(r) for r in rows]})

    elif action == 'low_stock':
        rows = conn.execute("""
            SELECT * FROM products 
            WHERE stock_quantity <= 10 AND is_active = 1
            ORDER BY stock_quantity ASC
            LIMIT 10
        """).fetchall()

        conn.close()
        return jsonify({'success': True, 'data': [dict(r) for r in rows]})

    elif action == 'recent_invoices':
        limit = int(request.args.get('limit', 5))
        rows = conn.execute("""
            SELECT * FROM invoices 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,)).fetchall()

        conn.close()
        return jsonify({'success': True, 'data': [dict(r) for r in rows]})

    elif action == 'hourly_sales':
        data = []
        for h in range(24):
            start_h = today.replace(hour=h, minute=0, second=0)
            end_h = today.replace(hour=h, minute=59, second=59)
            start_str = start_h.strftime('%Y-%m-%d %H:%M:%S')
            end_str = end_h.strftime('%Y-%m-%d %H:%M:%S')

            row = conn.execute("""
                SELECT COALESCE(SUM(total_amount), 0) as revenue, COUNT(*) as count
                FROM invoices WHERE created_at >= ? AND created_at <= ?
            """, (start_str, end_str)).fetchone()

            data.append({
                'hour': h,
                'revenue': row['revenue'],
                'count': row['count']
            })

        conn.close()
        return jsonify({'success': True, 'data': data})

    conn.close()
    return jsonify({'success': False, 'message': 'Unknown analytics action'})
