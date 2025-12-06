from flask import Blueprint, render_template, redirect, url_for, request
from src.app.models.product_model import ProductModel

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def index():
    return redirect(url_for('admin.products'))

@admin_bp.route('/products')
def products():
    all_products = ProductModel.get_all_products()
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
        ProductModel.add_product(data)
        return redirect(url_for('admin.products'))
    return render_template('admin/product_form.html')


@admin_bp.route('/delete/<id>')
def delete_product(id):
    ProductModel.delete_product(id)
    return redirect(url_for('admin.products'))