from flask import Blueprint, render_template, redirect, url_for, request
from src.app.models.product_model import ProductModel

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def index():
    return redirect(url_for('admin.products'))

@admin_bp.route('/products', methods=['GET'])
def products():
    search_query = request.args.get('q') 
    all_products = ProductModel.get_all_products()
    
    if search_query:
        query = search_query.strip().lower()
        filtered_products = [
            p for p in all_products
            if query in p['name'].lower() or query in p['category'].lower()
        ]
        return render_template('admin/search_results.html', products=filtered_products, query=search_query)
        
    return render_template('admin/products.html', products=all_products, query=None)

@admin_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        data = {
            'name': request.form.get('name'),
            'category': request.form.get('category'),
            'price': request.form.get('price'),
            'stock': request.form.get('stock'),
            'image': request.form.get('image')
        }
        ProductModel.add_product(data)
        return redirect(url_for('admin.products'))
    return render_template('admin/product_form.html') 

@admin_bp.route('/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == 'POST':
        data = {
            'id': product_id, 
            'name': request.form.get('name'),
            'category': request.form.get('category'),
            'price': request.form.get('price'),
            'stock': request.form.get('stock'),
            'image': request.form.get('image')
        }
        ProductModel.update_product(data)
        return redirect(url_for('admin.products'))

    product = ProductModel.get_product_by_id(product_id)
    if product is None:
        return redirect(url_for('admin.products'))
        
    return render_template('admin/product_edit_form.html', product=product) 

@admin_bp.route('/delete/<id>')
def delete_product(id):
    ProductModel.delete_product(id)
    return redirect(url_for('admin.products'))