import csv
import os

class ProductModel:
    @staticmethod
    def get_csv_file_path():
        return r"C:\Users\dreams\Desktop\copy of admin\data\pharmacy_ai_data_500.csv"

    @staticmethod
    def get_all_products():
        path = ProductModel.get_csv_file_path()
        products = []
        try:
            if not os.path.exists(path): return []
            
            with open(path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if not row or not row.get('id'): continue
                    products.append({
                        'id': row.get('id'),
                        'name': row.get('name_en', 'Unknown'),
                        'category': row.get('category', '-'),
                        'price': row.get('price', '0'),
                        'stock': row.get('stock_quantity', '0'),
                        'image': row.get('image_url', '')
                    })
            return products
        except Exception as e:
            return []

    @staticmethod
    def get_product_by_id(product_id):
        all_products = ProductModel.get_all_products()
        for p in all_products:
            if str(p['id']) == str(product_id):
                return p
        return None

    @staticmethod
    def add_product(data):
        path = ProductModel.get_csv_file_path()
        try:
            all_rows = []
            if os.path.exists(path):
                with open(path, mode='r', encoding='utf-8-sig') as f:
                    reader = csv.DictReader(f)
                    fieldnames = reader.fieldnames
                    for row in reader:
                        all_rows.append(row)

            new_id = 1
            if all_rows:
                ids = [int(r['id']) for r in all_rows if r.get('id') and str(r['id']).isdigit()]
                if ids: new_id = max(ids) + 1

            new_row = {
                'id': str(new_id),
                'name_en': data['name'],
                'category': data['category'],
                'price': str(data['price']),
                'stock_quantity': str(data['stock']),
                'image_url': data.get('image', ''),
                'sku': f'PROD-{new_id}', 'name_ar': data['name'], 'description_en': '', 'description_ar': '', 'barcode': '', 'expiry_date': '', 'is_active': '1'
            }
            
            for field in fieldnames:
                if field not in new_row: new_row[field] = ''
            
            all_rows.append(new_row)

            with open(path, mode='w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_rows)
            return True
        except Exception as e:
            return False

    @staticmethod
    def update_product(data):
        path = ProductModel.get_csv_file_path()
        all_rows = []
        updated = False
        
        try:
            with open(path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                for row in reader:
                    if str(row.get('id')) == str(data['id']):
                        row['name_en'] = data['name']
                        row['category'] = data['category']
                        row['price'] = data['price']
                        row['stock_quantity'] = data['stock']
                        row['image_url'] = data['image']
                        updated = True
                    all_rows.append(row)

            if updated:
                with open(path, mode='w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(all_rows)
                return True
            return False
        except Exception as e:
            return False

    @staticmethod
    def delete_product(product_id):
        path = ProductModel.get_csv_file_path()
        rows = []
        try:
            with open(path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                for row in reader:
                    if str(row.get('id')) != str(product_id):
                        rows.append(row)
            
            with open(path, mode='w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            return True
        except:
            return False