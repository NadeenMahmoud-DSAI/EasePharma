# src/scripts/create_admin.py
import os
import csv
import getpass
from werkzeug.security import generate_password_hash

# --- FIX: ROBUST PATH FINDING ---
# 1. Get the folder where THIS script lives (src/scripts)
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go up one level to 'src'
src_dir = os.path.dirname(current_script_dir)

# 3. Point to 'data' inside 'src'
DATA_DIR = os.path.join(src_dir, 'data')

USERS_FILE = os.path.join(DATA_DIR, 'users.csv')
FIELDNAMES = ['user_id', 'email', 'password_hash', 'role', 'full_name', 'phone', 'address']

def ensure_users_csv():
    if not os.path.exists(DATA_DIR):
        print(f"❌ Error: Data directory not found at {DATA_DIR}")
        return False
    
    if not os.path.exists(USERS_FILE):
        print(f"⚠️ Users file not found. Creating new one at {USERS_FILE}")
        with open(USERS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
    return True

def read_existing_users():
    users = []
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                users.append(r)
    return users

def write_users(users):
    with open(USERS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for u in users:
            writer.writerow(u)

def create_admin(email: str, password: str):
    users = read_existing_users()

    # Check if email already exists
    for u in users:
        if u['email'] == email:
            print(f"❌ Error: User {email} already exists!")
            return

    # Generate ID
    numeric_ids = [int(u['user_id']) for u in users if u.get('user_id') and u['user_id'].isdigit()]
    new_id = str(max(numeric_ids) + 1) if numeric_ids else '1001'

    pw_hash = generate_password_hash(password)
    
    new_user = {
        'user_id': new_id,
        'email': email,
        'password_hash': pw_hash,
        'role': 'Admin',  # Note: Capital 'A' to match your Auth Controller
        'full_name': 'Manual Admin',
        'phone': '',
        'address': ''
    }

    users.append(new_user)
    write_users(users)

    print(f"\n✅ SUCCESS! Admin created.")
    print(f"   File updated: {USERS_FILE}")
    print(f"   Login: {email}")
    print(f"   Role: Admin")

if __name__ == "__main__":
    if ensure_users_csv():
        print(f"Target Database: {USERS_FILE}")
        
        email = input("Enter Admin Email: ").strip()
        
        # PASSWORD INPUT LOOP
        while True:
            # Remember: Typing will be invisible!
            pwd = getpass.getpass("Enter Password (hidden): ").strip()
            if len(pwd) < 4:
                print("Too short. Try again.")
                continue
                
            pwd2 = getpass.getpass("Confirm Password (hidden): ").strip()
            if pwd != pwd2:
                print("Passwords do not match. Try again.")
                continue
            
            break

        create_admin(email, pwd)