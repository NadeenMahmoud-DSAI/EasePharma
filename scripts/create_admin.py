import csv
import os
import getpass
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'src', 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.csv')

FIELDNAMES = [
    'user_id', 'email', 'password_hash', 'role', 
    'full_name_en', 'phone', 'address', 'status', 
    'age', 'gender', 'governorate', 'city', 
    'join_date', 'total_spent', 'first_name_ar', 'last_name_ar'
]

def get_users():
    if not os.path.exists(USERS_FILE):
        return []
    
    with open(USERS_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_users(users):
    os.makedirs(DATA_DIR, exist_ok=True)
    
    with open(USERS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        
        for u in users:
            row_to_write = {field: u.get(field, '') for field in FIELDNAMES}
            writer.writerow(row_to_write)

def create_admin(email, password):
    users = get_users()
    
    for u in users:
        if u['email'].lower() == email.lower():
            print(f"User {email} already exists. Updating role to Admin...")
            u['role'] = 'Admin'
            u['password_hash'] = generate_password_hash(password)
            write_users(users)
            print("Admin updated successfully.")
            return

    print(f"Creating new admin user: {email}")
    new_admin = {
        'user_id': uuid.uuid4().hex[:10],
        'email': email,
        'password_hash': generate_password_hash(password),
        'role': 'Admin',
        'full_name_en': 'System Admin',
        'status': 'Active',
        'join_date': datetime.now().strftime('%Y-%m-%d'),
        'total_spent': '0.0',
        'phone': '', 'address': '', 'age': '', 'gender': '',
        'governorate': '', 'city': '', 'first_name_ar': '', 'last_name_ar': ''
    }
    
    users.append(new_admin)
    write_users(users)
    print("Admin created successfully.")

if __name__ == "__main__":
    print("--- Create Admin User ---")
    email = input("Admin email (default: admin@gmail.com): ").strip()
    if not email:
        email = "admin@gmail.com"
        
    pwd = getpass.getpass("Admin password (min 6 chars): ")
    confirm = getpass.getpass("Confirm password: ")
    
    if len(pwd) < 6:
        print("Error: Password must be at least 6 characters.")
    elif pwd != confirm:
        print("Error: Passwords do not match.")
    else:
        create_admin(email, pwd)