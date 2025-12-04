import os
import pandas as pd
from types import SimpleNamespace
from flask import current_app

class ProductModel:
    @staticmethod
    def _file(data_path):
        return os.path.join(data_path, 'products.csv')

    @classmethod
    def _read_df(cls, data_path):
        path = cls._file(data_path)
        if os.path.exists(path):
            return pd.read_csv(path)
        return pd.DataFrame()

    @classmethod
    def next_id(cls, data_path):
        df = cls._read_df(data_path)
        if df.empty:
            return 1
        return int(df['id'].max()) + 1

    @classmethod
    def append_product(cls, data_path, rowdict):
        path = cls._file(data_path)
        df = pd.DataFrame([rowdict])
        if not os.path.exists(path):
            df.to_csv(path, index=False)
        else:
            df.to_csv(path, mode='a', header=False, index=False)

    @classmethod
    def get_all(cls, data_path, limit=20):
        df = cls._read_df(data_path)
        if df.empty:
            return []
        rows = df.head(limit).to_dict(orient='records')
        products = []
        for r in rows:
            p = SimpleNamespace(
                id=int(r.get('id')),
                sku=r.get('sku',''),
                name=r.get('name_en') or r.get('name') or '',
                price=float(r.get('price', 0) or 0),
                stock=int(r.get('stock_quantity', r.get('stock', 0) or 0)),
                category=r.get('category',''),
                image=r.get('image',''),
                description=r.get('description_en','')
            )
            products.append(p)
        return products

    @classmethod
    def search(cls, data_path, keyword):
        df = cls._read_df(data_path)
        if df.empty or not keyword:
            return []
        mask = df['name_en'].astype(str).str.contains(keyword, case=False, na=False) | df['category'].astype(str).str.contains(keyword, case=False, na=False)
        rows = df[mask].to_dict(orient='records')
        return [SimpleNamespace(
                    id=int(r.get('id')),
                    sku=r.get('sku',''),
                    name=r.get('name_en') or r.get('name',''),
                    price=float(r.get('price',0) or 0),
                    stock=int(r.get('stock_quantity', r.get('stock', 0) or 0)),
                    category=r.get('category',''),
                    image=r.get('image',''),
                    description=r.get('description_en','')
                ) for r in rows]

    @classmethod
    def get_by_id(cls, data_path, prod_id):
        df = cls._read_df(data_path)
        if df.empty:
            return None
        row = df[df['id'] == int(prod_id)]
        if row.empty:
            return None
        r = row.iloc[0].to_dict()
        return SimpleNamespace(
            id=int(r.get('id')),
            sku=r.get('sku',''),
            name=r.get('name_en') or r.get('name',''),
            price=float(r.get('price',0) or 0),
            stock=int(r.get('stock_quantity', r.get('stock', 0) or 0)),
            category=r.get('category',''),
            image=r.get('image',''),
            description=r.get('description_en','')
        )

    @classmethod
    def decrement_stock(cls, data_path, prod_id, qty=1):
        path = cls._file(data_path)
        df = cls._read_df(data_path)
        if df.empty:
            return False
        idx = df.index[df['id'] == int(prod_id)].tolist()
        if not idx:
            return False
        i = idx[0]
        cur = int(df.at[i, 'stock_quantity']) if 'stock_quantity' in df.columns else int(df.at[i,'stock'])
        df.at[i, 'stock_quantity'] = max(0, cur - qty)
        df.to_csv(path, index=False)
        return True
