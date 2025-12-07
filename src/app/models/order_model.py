import os
import pandas as pd
from datetime import datetime
import uuid
from app.models.product_model import ProductModel
from types import SimpleNamespace

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
        # Calculate total and check stock
        for pid, qty in cart.items():
            p = ProductModel.get_by_id(data_path, int(pid))
            if not p: continue
            qty = int(qty)
            items.append(f"{p.name} (x{qty})")
            total += p.price * qty
            # Decrement stock
            ProductModel.decrement_stock(data_path, int(pid), qty)
        
        order_id = uuid.uuid4().hex[:8]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        items_summary = ", ".join(items)
        
        # Save to CSV
        new_row = {
            'order_id': order_id,
            'user_id': user_id,
            'items_summary': items_summary,
            'total_amount': total,
            'status': 'Pending',
            'created_at': now
        }
        df = pd.DataFrame([new_row])
        path = cls._file(data_path)
        
        if not os.path.exists(path):
            df.to_csv(path, index=False)
        else:
            df.to_csv(path, mode='a', header=False, index=False)
            
        return cls(order_id, user_id, items_summary, total, 'Pending', now)

    @classmethod
    def get_by_user(cls, data_path, user_id):
        path = cls._file(data_path)
        if not os.path.exists(path): return []
        try:
            df = pd.read_csv(path)
            # Filter by user_id
            user_orders = df[df['user_id'].astype(str) == str(user_id)]
            return [cls(r['order_id'], r['user_id'], r['items_summary'], r['total_amount'], r['status'], r['created_at']) for _, r in user_orders.iterrows()]
        except: return []
        
    @classmethod
    def get_all(cls, data_path):
        path = cls._file(data_path)
        if not os.path.exists(path): return []
        try:
            df = pd.read_csv(path)
            return [cls(r['order_id'], r['user_id'], r['items_summary'], r['total_amount'], r['status'], r['created_at']) for _, r in df.iterrows()]
        except: return []