import sys
import os
from flask import session, redirect, url_for, Blueprint

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import create_app

app = create_app()

# --- DEV TOOLS FOR MENNA (Role Switcher) ---
auth_test_bp = Blueprint('auth_test', __name__)

@auth_test_bp.route('/')
def login_menu():
    return """
    <div style="text-align:center; padding-top:50px; font-family:sans-serif;">
        <h1>Menna's Dev Environment</h1>
        <h3>Who do you want to be?</h3>
        <a href='/login/customer' style="background:#008080; color:white; padding:15px; text-decoration:none; border-radius:5px; margin:10px;">
            Login as Customer (Nadeen)
        </a>
        <a href='/login/admin' style="background:#333; color:white; padding:15px; text-decoration:none; border-radius:5px; margin:10px;">
            Login as Admin (Boss)
        </a>
    </div>
    """

@auth_test_bp.route('/login/customer')
def login_customer():
    session['user_id'] = '1001'
    session['role'] = 'Customer'
    session['user_name'] = 'Nadeen'
    return redirect(url_for('support.index'))

@auth_test_bp.route('/login/admin')
def login_admin():
    session['user_id'] = '9999'
    session['role'] = 'Admin'
    session['user_name'] = 'System Admin'
    return redirect(url_for('admin.inbox'))

app.register_blueprint(auth_test_bp)
# -------------------------------------------

if __name__ == '__main__':
    print("🚀 Running Menna's Feature on http://127.0.0.1:5002")
    app.run(debug=True, port=5002)