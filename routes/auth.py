from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash , session
from werkzeug.security import generate_password_hash, check_password_hash
from database import connect_db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]  # Store user ID in session
            flash("Login successful!", "success")
            return redirect(url_for('seller.dashboard'))

        flash("Invalid credentials", "danger")

    return render_template('login.html')

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        
        conn = connect_db()
        cursor = conn.cursor()
        
        # Insert user
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        user_id = cursor.lastrowid
        
        # Set 7-day trial period
        trial_end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO sellers (user_id, subscription_active, trial_end_date) VALUES (?, ?, ?)", (user_id, 0, trial_end_date))
        
        conn.commit()
        conn.close()
        
        flash("Registration successful! You have a 7-day free trial.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")
