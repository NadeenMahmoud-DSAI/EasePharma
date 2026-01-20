import os
import pandas as pd
from types import SimpleNamespace
from flask import current_app
import uuid 

class ProductModel:
    
    @staticmethod
    def _safe_float(value, default=0.0):
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def _safe_int(value, default=0):
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def _file(data_path):
        return os.path.join(data_path, 'products.csv')

    @classmethod
    def _read_df(cls, data_path):
        path = cls._file(data_path)
        if os.path.exists(path):
            return pd.read_csv(path, dtype=str)
        return pd.DataFrame()

    @classmethod
    def next_id(cls, data_path):
        df = cls._read_df(data_path)
        if df.empty: return 1
        ids = pd.to_numeric(df['id'], errors='coerce')
        return int(ids.max()) + 1 if not ids.dropna().empty else 1


    @classmethod
    def get_all(cls, data_path, limit=20):
        df = cls._read_df(data_path)
        if df.empty: return []
        
        rows = df.head(limit).to_dict(orient='records')
        products = []
        
        for r in rows:
            price = cls._safe_float(r.get('price'))
            
            if price <= 0:
                continue 
            
            p = SimpleNamespace(
                id=cls._safe_int(r.get('id')),
                sku=str(r.get('sku','')),
                name=str(r.get('name_en') or r.get('name') or ''),
                price=price,
                stock=cls._safe_int(r.get('stock_quantity') or r.get('stock')),
                category=str(r.get('category','')),
                image=str(r.get('image_url') or r.get('image') or ''),
                description=str(r.get('description_en',''))
            )
            products.append(p)
        return products

    @classmethod
    def search(cls, data_path, keyword):
        df = cls._read_df(data_path)
        if df.empty or not keyword: return []
        
        mask = df['name_en'].astype(str).str.contains(keyword, case=False, na=False) | \
               df['category'].astype(str).str.contains(keyword, case=False, na=False)
        rows = df[mask].to_dict(orient='records')
        
        results = []
        for r in rows:
            price = cls._safe_float(r.get('price'))
            
            if price <= 0:
                continue

            p = SimpleNamespace(
                id=cls._safe_int(r.get('id')),
                sku=str(r.get('sku','')),
                name=str(r.get('name_en') or r.get('name','')),
                price=price,
                stock=cls._safe_int(r.get('stock_quantity') or r.get('stock')),
                category=str(r.get('category','')),
                image=str(r.get('image_url') or r.get('image') or ''),
                description=str(r.get('description_en',''))
            )
            results.append(p)
        return results

    @classmethod
    def get_by_id(cls, data_path, prod_id):
        df = cls._read_df(data_path)
        if df.empty: return None
        
        df['id_num'] = pd.to_numeric(df['id'], errors='coerce')
        row = df[df['id_num'] == int(prod_id)]
        
        if row.empty: return None
        r = row.iloc[0].to_dict()
        
        return SimpleNamespace(
            id=cls._safe_int(r.get('id')),
            sku=str(r.get('sku','')),
            name=str(r.get('name_en') or r.get('name','')),
            price=cls._safe_float(r.get('price')),
            stock=cls._safe_int(r.get('stock_quantity') or r.get('stock')),
            category=str(r.get('category','')),
            image=str(r.get('image_url') or r.get('image') or ''),
            description=str(r.get('description_en',''))
        )

    @classmethod
    def decrement_stock(cls, data_path, prod_id, qty=1):
        path = cls._file(data_path)
        df = cls._read_df(data_path)
        if df.empty: return False
        
        df['id_num'] = pd.to_numeric(df['id'], errors='coerce')
        idx = df.index[df['id_num'] == int(prod_id)].tolist()
        
        if not idx: return False
        i = idx[0]
        
        stock_col = 'stock_quantity' if 'stock_quantity' in df.columns else 'stock'
        cur = cls._safe_int(df.at[i, stock_col])
        
        df.at[i, stock_col] = max(0, cur - qty)
        
        if 'id_num' in df.columns:
            df = df.drop(columns=['id_num'])
            
        df.to_csv(path, index=False)
        return True

    
    @classmethod
    def delete_product(cls, data_path, product_id):
        path = cls._file(data_path)
        if not os.path.exists(path): return False
        
        df = cls._read_df(data_path)
        df = df[df['id'].astype(str) != str(product_id)]
        
        df.to_csv(path, index=False)
        return True
    
    @classmethod
    def add_product(cls, data_path, data):
        path = cls._file(data_path)
        new_id = cls.next_id(data_path)
        
        row = {
            'id': new_id,
            'name_en': data.get('name'),
            'category': data.get('category'),
            'price': cls._safe_float(data.get('price')), 
            'stock_quantity': cls._safe_int(data.get('stock')),
            'image_url': data.get('image'),
            'sku': f'PROD-{new_id}', 
            'is_active': 1,
        }
        
        df = cls._read_df(data_path)
        new_row_df = pd.DataFrame([row])
        
        if df.empty:
            df_final = new_row_df
        else:
            df_final = pd.concat([df, new_row_df], ignore_index=True)

        df_final.to_csv(path, index=False)
        return True
    
    @classmethod
    def update_product(cls, data_path, product_id, data):
        path = cls._file(data_path)
        if not os.path.exists(path): return False
        
        df = cls._read_df(data_path)

        idx = df.index[df['id'].astype(str) == str(product_id)].tolist()
        if not idx: return False
        
        i = idx[0]
        
        df.at[i, 'name_en'] = data.get('name')
        df.at[i, 'category'] = data.get('category')
        df.at[i, 'price'] = cls._safe_float(data.get('price'))
        
        stock_col = 'stock_quantity' if 'stock_quantity' in df.columns else 'stock'
        df.at[i, stock_col] = cls._safe_int(data.get('stock'))
        
        df.at[i, 'image_url'] = data.get('image')
        
        df.to_csv(path, index=False)
        return True