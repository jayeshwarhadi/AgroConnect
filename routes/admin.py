from flask import Blueprint, render_template, redirect, url_for, flash
from database import connect_db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_dashboard():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sellers")
    sellers = cursor.fetchall()
    conn.close()
    
    return render_template('admin_dashboard.html', sellers=sellers)

@admin_bp.route('/admin/delete_seller/<int:seller_id>')
def delete_seller(seller_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sellers WHERE id = ?", (seller_id,))
    conn.commit()
    conn.close()

    flash("Seller deleted!", "danger")
    return redirect(url_for('admin.admin_dashboard'))
