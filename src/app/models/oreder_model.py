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
            if not p:
                continue
            qty = int(qty)
            items.append({'id': p.id, 'name': p.name, 'qty': qty, 'unit_price': p.price})
            total += p.price * qty
        order_id = uuid.uuid4().hex[:10]
        now = datetime.utcnow().isoformat()
        items_summary = str(items)
        df = pd.DataFrame([{
            'order_id': order_id,
            'user_id': user_id,
            'items_summary': items_summary,
            'total_amount': total,
            'status': 'Pending',
            'created_at': now
        }])
        path = cls._file(data_path)
        if not os.path.exists(path):
            df.to_csv(path, index=False)
        else:
            df.to_csv(path, mode='a', header=False, index=False)
        # decrement stock
        for it in items:
            ProductModel.decrement_stock(data_path, it['id'], it['qty'])
        return cls(order_id, user_id, items_summary, total, 'Pending', now)

    @classmethod
    def get_by_user(cls, data_path, user_id):
        path = cls._file(data_path)
        if not os.path.exists(path):
            return []
        df = pd.read_csv(path)
        rows = df[df['user_id'] == user_id].to_dict(orient='records')
        return [cls(r['order_id'], r['user_id'], r['items_summary'], r['total_amount'], r['status'], r['created_at']) for r in rows]

    @classmethod
    def get_all(cls, data_path):
        path = cls._file(data_path)
        if not os.path.exists(path):
            return []
        df = pd.read_csv(path)
        rows = df.to_dict(orient='records')
        return [cls(r['order_id'], r['user_id'], r['items_summary'], r['total_amount'], r['status'], r['created_at']) for r in rows]

    @classmethod
    def update_status(cls, data_path, order_id, new_status):
        path = cls._file(data_path)
        if not os.path.exists(path):
            return False
        df = pd.read_csv(path)
        idx = df.index[df['order_id'] == order_id].tolist()
        if not idx:
            return False
        df.at[idx[0], 'status'] = new_status
        df.to_csv(path, index=False)
        return True
