import os
import json
from flask import Flask, request, render_template_string, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

# --- CONFIG ---
app = Flask(__name__)
app.secret_key = 'super_secret_final_key'
DATA_FILE = 'final_users.json'

# --- SINGLE HTML LAYOUT (Cannot be duplicated) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ease Pharma</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #f4f7f6; font-family: sans-serif; }
        .card { border: none; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .btn-teal { background: #008080; color: white; width: 100%; padding: 10px; }
        .btn-teal:hover { background: #006666; color: white; }
        .text-teal { color: #008080; }
    </style>
</head>
<body>
<div class="container mt-5">
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for msg in messages %}<div class="alert alert-info">{{ msg }}</div>{% endfor %}
        {% endif %}
    {% endwith %}

    {% if mode == 'login' %}
    <div class="row justify-content-center">
        <div class="col-md-4">
            <div class="card p-4">
                <h3 class="text-center mb-3 text-teal">Login</h3>
                <form method="POST" action="{{ url_for('login') }}">
                    <div class="mb-3"><label>Email</label><input type="email" name="email" class="form-control" required></div>
                    <div class="mb-3"><label>Password</label><input type="password" name="password" class="form-control" required></div>
                    <button class="btn btn-teal">Sign In</button>
                    <div class="text-center mt-3"><a href="{{ url_for('register') }}">Create Account</a></div>
                </form>
            </div>
        </div>
    </div>

    {% elif mode == 'register' %}
    <div class="row justify-content-center">
        <div class="col-md-4">
            <div class="card p-4">
                <h3 class="text-center mb-3 text-teal">Register</h3>
                <form method="POST" action="{{ url_for('register') }}">
                    <div class="mb-3"><label>Full Name</label><input type="text" name="full_name" class="form-control"></div>
                    <div class="mb-3"><label>Email</label><input type="email" name="email" class="form-control" required></div>
                    <div class="mb-3"><label>Password</label><input type="password" name="password" class="form-control" required></div>
                    <button class="btn btn-teal">Register</button>
                    <div class="text-center mt-3"><a href="{{ url_for('login') }}">Back to Login</a></div>
                </form>
            </div>
        </div>
    </div>

    {% elif mode == 'home' %}
    <div class="text-center mt-5">
        <h1 class="text-teal">Welcome, {{ user_name }}!</h1>
        <p class="lead">You are logged in.</p>
        <a href="{{ url_for('logout') }}" class="btn btn-danger">Logout</a>
    </div>
    {% endif %}
</div>
</body>
</html>
"""

# --- DATABASE ---
def get_users():
    if not os.path.exists(DATA_FILE): return []
    try:
        with open(DATA_FILE, 'r') as f: return json.load(f)
    except: return []

def save_user(user):
    users = get_users()
    users.append(user)
    with open(DATA_FILE, 'w') as f: json.dump(users, f, indent=4)

# --- ROUTES ---
@app.route('/')
def home():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template_string(HTML_TEMPLATE, mode='home', user_name=session.get('user_name', 'User'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').lower().strip()
        password = request.form.get('password')
        user = next((u for u in get_users() if u['email'] == email), None)
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['email']
            session['user_name'] = user.get('full_name', 'User')
            return redirect(url_for('home'))
        flash("Invalid email or password.")
        
    return render_template_string(HTML_TEMPLATE, mode='login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email').lower().strip()
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        
        if any(u['email'] == email for u in get_users()):
            flash("Email already exists.")
        else:
            save_user({'email': email, 'password': generate_password_hash(password), 'full_name': full_name})
            flash("Account created! Please login.")
            return redirect(url_for('login'))
            
    return render_template_string(HTML_TEMPLATE, mode='register')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Use Port 5002 to ensure it is unique and clean
    print("STARTING SERVER ON PORT 5002...")
    app.run(debug=True, port=5002)