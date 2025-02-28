from flask import Blueprint, render_template
from database import connect_db

public = Blueprint('public', __name__)

@public.route('/')
def home():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT products.id, products.name, products.description, products.price, users.username
        FROM products
        JOIN sellers ON products.seller_id = sellers.id
        JOIN users ON sellers.user_id = users.id
        WHERE sellers.subscription_active = 1
    """)
    products = cursor.fetchall()
    conn.close()

    return render_template('home.html', products=products)
