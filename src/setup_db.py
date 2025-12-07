import pandas as pd
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

FILE_USERS = os.path.join(BASE_DIR, "customers_with_age_1000.csv")
FILE_PRODUCTS = os.path.join(BASE_DIR, "pharmacy_ai_data_5000.csv")
FILE_ORDERS = os.path.join(BASE_DIR, "orders_transactions_1000.csv")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


# 1. USERS
if os.path.exists(FILE_USERS):
    try:
        df = pd.read_csv(FILE_USERS)
        if 'password_hash' not in df.columns:
            df['password_hash'] = generate_password_hash('123456')
        if 'role' not in df.columns:
            df['role'] = 'Customer'
            df.loc[df['user_id'] == 1001, 'role'] = 'Admin'
            
        df.to_csv(os.path.join(DATA_DIR, 'users.csv'), index=False)
    except: pass

# 2. PRODUCTS
if os.path.exists(FILE_PRODUCTS):
    try:
        df = pd.read_csv(FILE_PRODUCTS)
        df['image_url'] = "https://placehold.co/400x400/008080/ffffff?text=Product"
        df.to_csv(os.path.join(DATA_DIR, 'products.csv'), index=False)
        print(f"Products restored ({len(df)} records).")
    except: pass

# 3. ORDERS
if os.path.exists(FILE_ORDERS):
    try:
        df = pd.read_csv(FILE_ORDERS)
        if 'customer_id' in df.columns:
            df.rename(columns={'customer_id': 'user_id'}, inplace=True)
        df.to_csv(os.path.join(DATA_DIR, 'orders.csv'), index=False)
        print(f"Orders restored.")
    except: pass
else:
    pd.DataFrame(columns=['order_id','user_id','total_amount','status']).to_csv(os.path.join(DATA_DIR, 'orders.csv'), index=False)