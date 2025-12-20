import os
import pandas as pd
from types import SimpleNamespace

class OrderModel:
    @staticmethod
    def _file(data_path):
        return os.path.join(data_path, 'orders.csv')

    @staticmethod
    def _safe_float(value):
        try:
            return float(str(value).replace(',', '').strip())
        except (ValueError, TypeError):
            return 0.0

    @classmethod
    def get_all(cls, data_path):
        path = cls._file(data_path)
        if not os.path.exists(path): 
            print("orders.csv not found at", path)
            return []
        
        try:
            df = pd.read_csv(path, dtype=str, on_bad_lines='skip')
            df = df.fillna('')
            
            orders = []
            for _, row in df.iterrows():
                oid = row.get('order_id', 'Unknown')
                uid = row.get('user_id', 'Unknown')
                possible_price = cls._safe_float(row.get('status'))
                
                if possible_price > 0:
                    price = possible_price
                    status = row.get('payment_method', 'Pending') 
                    items = row.get('order_date', '')     
                    date_val = row.get('total_amount', '') 
                else:
                    price = cls._safe_float(row.get('total_amount'))
                    status = row.get('status', 'Pending')
                    items = row.get('items_summary', '')
                    date_val = row.get('order_date', '')

                if status not in ['Pending', 'Shipped', 'Delivered', 'Cancelled']:
                    status = 'Pending'

                o = SimpleNamespace(
                    order_id=oid,
                    user_id=uid,
                    items_summary=items,
                    total_amount=price,
                    status=status,
                    created_at=date_val
                )
                orders.append(o)
            
            return orders

        except Exception as e:
            print(f"ERROR reading orders: {e}")
            return []

    @classmethod
    def update_status(cls, data_path, order_id, new_status):
        path = cls._file(data_path)
        if not os.path.exists(path): return False
        try:
            df = pd.read_csv(path, dtype=str)
            mask = df['order_id'] == str(order_id)
            if mask.any():
                df.loc[mask, 'status'] = new_status 
                df.to_csv(path, index=False)
                return True
            return False
        except: return False