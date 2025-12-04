from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_model import UserModel
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def password_valid(p):
    return len(p) >= 8

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email','').strip().lower()
        password = request.form.get('password','')

        user = UserModel.get_by_email(email, current_app.config['DATA_PATH'])

        if user and check_password_hash(user.get('password_hash',''), password):
            session.clear()
            session['user_id'] = user.get('user_id') or user.get('email')
            session['role'] = user.get('role','Customer')
            flash("Login successful")
            if session['role'] == 'Admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('product.home'))
        else:
            # simple counter for failed attempts (session based)
            session['failed_login'] = session.get('failed_login', 0) + 1
            if session['failed_login'] >= 5:
                flash("Too many failed attempts. Try again later.")
            else:
                flash("Invalid credentials")
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email','').strip().lower()
        password = request.form.get('password','')
        name = request.form.get('full_name','').strip()
        phone = request.form.get('phone','').strip()
        address = request.form.get('address','').strip()

        if not password_valid(password):
            flash("Password must be at least 8 characters")
            return render_template('auth/register.html')

        if UserModel.get_by_email(email, current_app.config['DATA_PATH']):
            flash('Email already exists')
            return render_template('auth/register.html')

        hashed = generate_password_hash(password)
        user = UserModel(email=email, password_hash=hashed, full_name=name, phone=phone, address=address)
        user.save(current_app.config['DATA_PATH'])
        flash('Registration successful! Please login.')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out")
    return redirect(url_for('product.home'))
