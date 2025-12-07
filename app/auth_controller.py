import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_model import UserModel

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        data_path = current_app.config['DATA_PATH']
        user = UserModel.get_by_email(email, data_path)

        if user and check_password_hash(user.get('password_hash', ''), password):
            session.clear()
            session['user_id'] = user.get('user_id')
            session['role'] = user.get('role', 'Customer')
            flash('Welcome back!')
            return redirect(url_for('product.home'))
        else:
            flash('Invalid email or password.')
            
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        data_path = current_app.config['DATA_PATH']

        if UserModel.get_by_email(email, data_path):
            flash('Email already exists')
        else:
            hashed = generate_password_hash(password)
            user = UserModel(email=email, password_hash=hashed, full_name='', phone='', address='')
            user.save(data_path)
            
            flash('Registration successful! Please sign in.')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')
