from __main__ import app
from flask import Flask, render_template, url_for, session, request, redirect, flash
from hashlib import md5
from db_connector import database

db = database()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone", "")

        # Basic validation
        if not all([first_name, last_name, email, password]):
            flash('All fields are required', 'danger')
            return redirect(url_for('register'))
            
        # Check if email already exists
        existing_user = db.queryDB("SELECT * FROM users WHERE email = ?", [email])
        if existing_user:
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))

        # Hash password
        hashed_password = md5(password.encode()).hexdigest()
        
        try:
            # Insert new user
            db.updateDB(
                "INSERT INTO users (Firstname, Lastname, Email, Password, Phone) VALUES (?, ?, ?, ?, ?)",
                (first_name, last_name, email, hashed_password, phone)
            )
            
            # Get the new user's data and auto-login
            user = db.queryDB("SELECT * FROM users WHERE email = ?", [email])
            if user:
                # Store all user data in session
                session['user_id'] = user[0]['id']
                session['email'] = user[0]['Email']
                session['first_name'] = user[0]['Firstname']
                
                flash('Registration successful! You are now logged in.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Error creating user account', 'danger')
                return redirect(url_for('register'))
                
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Hash the password to match the stored hash
        hashed_password = md5(password.encode()).hexdigest()
        
        # Query the database for the user
        user = db.queryDB("SELECT * FROM users WHERE email = ?", [email])
        
        if user and user[0]['Password'] == hashed_password:
            # Store user in session
            # session['user_id'] = user[0]['id']
            session['email'] = user[0]['Email']
            session['first_name'] = user[0]['Firstname']
            
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        flash('Please log in to access this page', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/accessibility')
def accessibility():
    return render_template('accessibility.html')

@app.route('/premium', methods=['GET', 'POST'])
def premium():
    if 'email' not in session:
        flash('Please log in to access the premium page', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            # Get form data
            fullname = request.form["fullname"]
            email = request.form["email"]
            address = request.form["address"]
            city = request.form["city"]
            postcode = request.form["postcode"]
            cardholder_name = request.form["cardholder_name"]
            card_number = request.form["card_number"]
            expiry_month = request.form["expiry_month"]
            expiry_year = request.form["expiry_year"]
            cvv = request.form["cvv"]
            
            # Basic validation
            if not all([fullname, email, address, city, postcode, cardholder_name, card_number, expiry_month, expiry_year, cvv]):
                flash('All fields are required', 'danger')
                return redirect(url_for('premium'))
            
            # Insert into database (adjust table name and columns as needed)
            db.updateDB(
                "INSERT INTO Premium (Fullname, Email, Address, City, Postcode, CardholderName, CardNumber, ExpiryMonth, ExpiryYear, CVV) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (fullname, email, address, city, postcode, cardholder_name, card_number, expiry_month, expiry_year, cvv)
            )
            
            flash('Premium subscription successful!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            flash(f'Error processing payment: {str(e)}', 'danger')
            return redirect(url_for('premium'))
    
    return render_template('premium_page.html')