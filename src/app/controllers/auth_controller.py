import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_model import UserModel

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_data_path():
    return current_app.config['DATA_PATH']

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        data_path = get_data_path()
        user = UserModel.get_by_email(email, data_path)

        if user and check_password_hash(user.get('password_hash', ''), password):
            session.clear()
            session['user_id'] = user.get('user_id')
            session['role'] = user.get('role', 'Customer')
            session['user_name'] = user.get('full_name_en') or user.get('first_name_ar') or 'Valued Customer'
            flash(f"Welcome back, {session['user_name']}!")

            if session['role'] == 'Admin':
                return redirect(url_for('admin.products'))
            
            return redirect(url_for('product.home'))
        else:
            flash("Invalid email or password.")
            
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()

        data_path = get_data_path()

        if UserModel.get_by_email(email, data_path):
            flash('Email already exists')
        else:
            hashed = generate_password_hash(password)
            user = UserModel(email=email, password_hash=hashed, full_name=full_name, phone=phone, address=address)
            user.save(data_path)
            
            flash('Registration successful! Please sign in.')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out.")
    return redirect(url_for('auth.login'))