import os
import json
from flask import Flask, request, render_template_string, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

# --- CONFIGURATION ---
app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATA_FILE = 'users.json'  # This file will be created automatically

# --- IN-MEMORY HTML TEMPLATES (No folders needed) ---

BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ease Pharma</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root { --teal: #008080; }
        body { background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .text-teal { color: var(--teal); }
        .btn-teal { background-color: var(--teal); color: white; border: none; }
        .btn-teal:hover { background-color: #006666; color: white; }
    </style>
</head>
<body>
    <div class="container mt-5">
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-info">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

LOGIN_HTML = """
{% extends "layout" %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-5 col-lg-4">
        <div class="card shadow border-0">
            <div class="card-body p-4">
                <h3 class="text-center mb-4 text-teal">Login</h3>
                <form method="POST">
                    <div class="mb-3">
                        <label class="form-label small text-muted">Email</label>
                        <input type="email" name="email" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label small text-muted">Password</label>
                        <input type="password" name="password" class="form-control" required>
                    </div>
                    <button type="submit" class="btn btn-teal w-100 py-2">Login</button>
                    <div class="text-center mt-3">
                        <small>No account? <a href="{{ url_for('register') }}" class="text-teal">Register</a></small>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

REGISTER_HTML = """
{% extends "layout" %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-5">
        <div class="card shadow border-0">
            <div class="card-body p-4">
                <h3 class="text-center mb-4 text-teal">Register</h3>
                <form method="POST">
                    <div class="mb-3"><label class="small text-muted">Full Name</label><input type="text" name="full_name" class="form-control"></div>
                    <div class="mb-3"><label class="small text-muted">Email</label><input type="email" name="email" class="form-control" required></div>
                    <div class="mb-3"><label class="small text-muted">Password</label><input type="password" name="password" class="form-control" required></div>
                    <button type="submit" class="btn btn-teal w-100 py-2">Create Account</button>
                    <div class="text-center mt-3">
                        <small>Already have an account? <a href="{{ url_for('login') }}" class="text-teal">Login</a></small>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

HOME_HTML = """
{% extends "layout" %}
{% block content %}
<div class="text-center mt-5">
    <h1 class="text-teal">Welcome, {{ session.get('user_name', 'User') }}!</h1>
    <p class="lead text-muted">You have successfully logged into Ease Pharma.</p>
    <hr class="my-4">
    <a href="{{ url_for('logout') }}" class="btn btn-danger px-4">Logout</a>
</div>
{% endblock %}
"""

# --- DATABASE HELPERS ---
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
    # Combine layout and page
    full_html = HOME_HTML.replace('{% extends "layout" %}', BASE_LAYOUT)
    return render_template_string(full_html)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        users = get_users()
        # Find user
        user = next((u for u in users if u['email'] == email), None)
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['email']
            session['user_name'] = user.get('full_name', 'User')
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password.")
            
    full_html = LOGIN_HTML.replace('{% extends "layout" %}', BASE_LAYOUT)
    return render_template_string(full_html)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        full_name = request.form.get('full_name', '')
        
        users = get_users()
        if any(u['email'] == email for u in users):
            flash("Email already exists.")
        else:
            hashed = generate_password_hash(password)
            save_user({'email': email, 'password': hashed, 'full_name': full_name})
            flash("Account created! Please login.")
            return redirect(url_for('login'))
            
    full_html = REGISTER_HTML.replace('{% extends "layout" %}', BASE_LAYOUT)
    return render_template_string(full_html)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Running on port 5001 to avoid conflicts
    app.run(debug=True, port=5555)