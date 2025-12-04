import pandas as pd
import os
from werkzeug.security import generate_password_hash

# Exact filenames you uploaded
USER_CSV_NAME = "customers_with_age_1000.csv"
PRODUCT_CSV_NAME = "products.csv"
ORDER_CSV_NAME = "orders_transactions_1000.csv"

def find_file(filename):
    # Check current folder
    if os.path.exists(filename): return filename
    # Check parent folder
    parent = os.path.join("..", filename)
    if os.path.exists(parent): return parent
    return None

# Ensure data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

print("--- Setting up Database ---")

# 1. USERS
f_user = find_file(USER_CSV_NAME)
if f_user:
    try:
        df = pd.read_csv(f_user)
        # Add password/role if missing
        if 'password_hash' not in df.columns:
            print("   -> Generating passwords...")
            df['password_hash'] = generate_password_hash('123456')
        if 'role' not in df.columns:
            df['role'] = 'Customer'
            df.loc[0, 'role'] = 'Admin' # First user is Admin
        
        df.to_csv('data/users.csv', index=False)
        print(f"✅ Users loaded from {f_user}")
    except Exception as e:
        print(f"❌ User Error: {e}")
else:
    print(f"⚠️  MISSING: {USER_CSV_NAME} (Move this file into 'src/')")

# 2. PRODUCTS
f_prod = find_file(PRODUCT_CSV_NAME)
if f_prod:
    try:
        df = pd.read_csv(f_prod)
        df.to_csv('data/products.csv', index=False)
        print(f"✅ Products loaded from {f_prod}")
    except Exception as e:
        print(f"❌ Product Error: {e}")
else:
    print(f"⚠️  MISSING: {PRODUCT_CSV_NAME}")

# 3. ORDERS
f_ord = find_file(ORDER_CSV_NAME)
if f_ord:
    try:
        df = pd.read_csv(f_ord)
        df.to_csv('data/orders.csv', index=False)
        print(f"✅ Orders loaded from {f_ord}")
    except: pass
else:
    # Create empty orders file so app doesn't crash
    pd.DataFrame(columns=['order_id', 'user_id', 'items_summary', 'total_amount', 'status']).to_csv('data/orders.csv', index=False)
    print("⚠️  Created empty orders.csv")