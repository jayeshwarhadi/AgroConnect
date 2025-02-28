import stripe
from flask import Blueprint, render_template, redirect, url_for, flash ,session
from datetime import datetime, timedelta
from database import connect_db
from config import Config

stripe.api_key = Config.STRIPE_SECRET_KEY
seller_bp = Blueprint('seller', __name__)

@seller_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("You must be logged in!", "danger")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sellers WHERE user_id = ?", (user_id,))
    seller = cursor.fetchone()
    conn.close()

    if not seller:
        flash("No seller account found.", "danger")
        return redirect(url_for('public.home'))

    return render_template('seller_dashboard.html', seller=seller)

@seller_bp.route('/subscribe')
def subscribe():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'Monthly Subscription'},
                'unit_amount': 1000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('seller.activate_subscription', _external=True),
        cancel_url=url_for('seller.dashboard', _external=True)
    )
    return redirect(session.url, code=303)

@seller_bp.route('/activate_subscription')
def activate_subscription():
    conn = connect_db()
    cursor = conn.cursor()
    expiry_date = (datetime.utcnow() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE sellers SET active_subscription = 1, subscription_expiry = ? WHERE user_id = ?", 
                   (expiry_date, 1))  # Replace 1 with logged-in user's ID
    conn.commit()
    conn.close()
    
    flash("Subscription activated!", "success")
    return redirect(url_for('seller.dashboard'))
