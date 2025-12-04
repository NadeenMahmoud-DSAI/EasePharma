from flask import Blueprint, render_template, session, redirect, url_for, flash, request, current_app
from app.models.product_model import ProductModel
from app.models.order_model import OrderModel
import os
import pandas as pd
import time

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
def require_admin():
    if 'user_id' not in session or session.get('role') != 'Admin':
        flash("Admins Only!")
        return redirect(url_for('auth.login'))

@admin_bp.route('/dashboard')
def dashboard():
    products = ProductModel.get_all(current_app.config['DATA_PATH'], limit=1000)
    low_stock = sum(1 for p in products if int(p.stock) <= 5)
    orders = OrderModel.get_all(current_app.config['DATA_PATH'])
    return render_template('admin/dashboard.html', products=products, total_products=len(products), low_stock=low_stock, orders=orders)

@admin_bp.route('/product/new', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        price = float(request.form.get('price', 0))
        stock = int(request.form.get('stock', 0))
        sku = request.form.get('sku','')
        image = request.form.get('image','')
        description = request.form.get('description','')

        ProductModel.append_product(current_app.config['DATA_PATH'], {
            'id': ProductModel.next_id(current_app.config['DATA_PATH']),
            'sku': sku,
            'name_en': name,
            'price': price,
            'stock_quantity': stock,
            'category': category,
            'image': image,
            'description_en': description
        })
        flash("Product added")
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_product.html')

@admin_bp.route('/orders/<order_id>/update', methods=['POST'])
def update_order(order_id):
    new_status = request.form.get('status','Processing')
    OrderModel.update_status(current_app.config['DATA_PATH'], order_id, new_status)
    flash("Order status updated")
    return redirect(url_for('admin.dashboard'))
