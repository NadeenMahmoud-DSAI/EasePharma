from flask import Blueprint, render_template, redirect, url_for, request, current_app, session, flash
from app.models.product_model import ProductModel

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def get_data_path():
    return current_app.config['DATA_PATH']

# Protect Admin Routes
@admin_bp.before_request
def require_admin():
    pass 

@admin_bp.route('/')
def index():
    return redirect(url_for('admin.products'))

@admin_bp.route('/products')
def products():
    all_products = ProductModel.get_all(get_data_path(), limit=1000)
    return render_template('admin/products.html', products=all_products)

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
        ProductModel.add_product(get_data_path(), data)
        flash("Product added successfully!")
        return redirect(url_for('admin.products'))
    return render_template('admin/product_form.html')

@admin_bp.route('/delete/<id>')
def delete_product(id):
    ProductModel.delete_product(get_data_path(), id)
    flash("Product deleted.")
    return redirect(url_for('admin.products'))
@admin_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == 'POST':
        # Gather data
        data = {
            'name': request.form.get('name'),
            'category': request.form.get('category'),
            'price': float(request.form.get('price', 0)),
            'stock': int(request.form.get('stock', 0)),
            'image': request.form.get('image')
        }
        
        # Call the model to update
        if ProductModel.update_product(get_data_path(), product_id, data):
            flash("Product updated successfully!")
        else:
            flash("Error updating product.")
            
        return redirect(url_for('admin.products'))
    
    # Find the product and show the form
    product = ProductModel.get_by_id(get_data_path(), product_id)
    if not product:
        flash("Product not found.")
        return redirect(url_for('admin.products'))
        
    return render_template('admin/edit_product.html', product=product)