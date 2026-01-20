import os
import pandas as pd
from datetime import datetime
import uuid
from app.models.product_model import ProductModel

class OrderModel:
    @staticmethod
    def _file(data_path):
        return os.path.join(data_path, 'orders.csv')

    def __init__(self, order_id, user_id, items_summary, total_amount, status, created_at):
        self.order_id = order_id
        self.user_id = user_id
        self.items_summary = items_summary
        self.total_amount = total_amount
        self.status = status
        self.created_at = created_at

    @classmethod
    def create_from_cart(cls, data_path, user_id, cart):
        items = []
        total = 0.0
        
        for pid, qty in cart.items():
            p = ProductModel.get_by_id(data_path, int(pid))
            if not p: continue
            
            qty = int(qty)
            items.append(f"{p.name} (x{qty})")
            total += p.price * qty
            ProductModel.decrement_stock(data_path, int(pid), qty)
        
        order_id = uuid.uuid4().hex[:8]
        now = datetime.now().strftime("%Y-%m-%d") 
        items_summary = " | ".join(items) 
        
        
        new_row = {
            'order_id': order_id,
            'customer_id': user_id,          
            'customer_name': 'Online User',  
            'order_date': now,               
            'status': 'Pending',
            'total_amount': total,
            'receipt_summary': items_summary 
        }
        
        path = cls._file(data_path)
        df = pd.DataFrame([new_row])
        
        if not os.path.exists(path):
            df.to_csv(path, index=False)
        else:
            df.to_csv(path, mode='a', header=False, index=False)
            
        return cls(order_id, user_id, items_summary, total, 'Pending', now)

    @classmethod
    def get_all(cls, data_path):
        path = cls._file(data_path)
        if not os.path.exists(path): return []
        try:
            df = pd.read_csv(path)
            df = df.fillna('')
            
            orders = []
            for _, r in df.iterrows():
                oid = r.get('order_id', 'Unknown')
                
                uid = r.get('customer_id') or r.get('user_id') or 'Guest'
                
                items = r.get('receipt_summary') or r.get('items_summary') or ''
                
                date_val = r.get('order_date') or r.get('created_at') or 'N/A'
                
                raw_status = r.get('status', 'Pending')
                if raw_status == 'Completed':
                    status = 'Delivered'
                else:
                    status = raw_status
                try:
                    amt = float(r.get('total_amount', 0))
                except:
                    amt = 0.0

                orders.append(cls(oid, uid, items, amt, status, date_val))
            
            return orders
        except Exception as e:
            print(f"Error reading orders: {e}")
            return []

    @classmethod
    def get_by_user(cls, data_path, user_id):
        orders = cls.get_all(data_path)
        return [o for o in orders if str(o.user_id) == str(user_id)]

    @classmethod
    def update_status(cls, data_path, order_id, new_status):
        path = cls._file(data_path)
        if not os.path.exists(path): return False
        try:
            df = pd.read_csv(path)
            df['order_id'] = df['order_id'].astype(str)
            
            idx = df.index[df['order_id'] == str(order_id)].tolist()
            if not idx: return False
            
            df.at[idx[0], 'status'] = new_status
            df.to_csv(path, index=False)
            return True
        except: return False