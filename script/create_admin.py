import os
import csv
import getpass
from werkzeug.security import generate_password_hash

# directory
base_dir = os.getcwd()
default_data = os.path.join(base_dir, 'src', 'data')
DATA_DIR = os.environ.get('DATA_PATH', default_data)

USERS_FILE = os.path.join(DATA_DIR, 'users.csv')
FIELDNAMES = ['user_id', 'email', 'password_hash', 'role']


def ensure_users_csv():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


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

    # max numeric id
    numeric_ids = [int(u['user_id']) for u in users if u.get('user_id') and u['user_id'].isdigit()]
    new_id = str(max(numeric_ids) + 1) if numeric_ids else '1'

    pw_hash = generate_password_hash(password)
    new_user = {
        'user_id': new_id,
        'email': email,
        'password_hash': pw_hash,
        'role': 'admin'
    }

    users.append(new_user)
    write_users(users)

    print(f"[OK] Admin created: {email} (id={new_id})")


if _name_ == "_main_":
    ensure_users_csv()
    print("Create an admin user for local testing.")
    
    default_email = "admin@ease.local"
    email = input(f"Admin email (default: {default_email}): ").strip() or default_email

    while True:
        pwd = getpass.getpass("Admin password (min 6 chars): ").strip()

        if len(pwd) < 6:
            print("Password too short — must be at least 6 characters.")
            continue

        pwd2 = getpass.getpass("Confirm password: ").strip()
        if pwd != pwd2:
            print("Passwords do not match — try again.")
            continue

        break

    create_admin(email, pwd)