from flask import Blueprint, render_template, redirect, url_for, request, current_app, session, flash
from app.models.product_model import ProductModel
from app.models.order_model import OrderModel

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def get_data_path():
    return current_app.config['DATA_PATH']

@admin_bp.before_request
def require_admin():
    if 'role' not in session or session['role'] != 'Admin':
        flash("Access Denied: Admins only.")
        return redirect(url_for('auth.login'))

@admin_bp.route('/')
def index():
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    data_path = get_data_path()
    
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        new_status = request.form.get('status')
        if order_id and new_status:
            OrderModel.update_status(data_path, order_id, new_status)
            flash(f"Order {order_id} updated to {new_status}")
            return redirect(url_for('admin.dashboard'))

    all_orders = OrderModel.get_all(data_path)
    
    total_revenue = sum(float(getattr(o, 'total_amount', 0) or 0) for o in all_orders if getattr(o, 'status', '') != 'Cancelled')
    pending_count = sum(1 for o in all_orders if getattr(o, 'status', '') == 'Pending')
    delivered_count = sum(1 for o in all_orders if getattr(o, 'status', '') == 'Delivered')
    total_orders = len(all_orders)
    
    return render_template('admin/dashboard.html', 
                           orders=all_orders,
                           stats={
                               'revenue': total_revenue,
                               'pending': pending_count,
                               'delivered': delivered_count,
                               'total': total_orders
                           })

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
        data = {
            'name': request.form.get('name'),
            'category': request.form.get('category'),
            'price': float(request.form.get('price', 0)),
            'stock': int(request.form.get('stock', 0)),
            'image': request.form.get('image')
        }
        if ProductModel.update_product(get_data_path(), product_id, data):
            flash("Product updated successfully!")
        else:
            flash("Error updating product.")
        return redirect(url_for('admin.products'))
    
    product = ProductModel.get_by_id(get_data_path(), product_id)
    if not product:
        flash("Product not found.")
        return redirect(url_for('admin.products'))
        
    return render_template('admin/edit_product.html', product=product)

@admin_bp.route('/support')
def support_inbox():
    return render_template('admin/support_inbox.html', users=[])

@admin_bp.route('/support/<user_id>', methods=['GET', 'POST'])
def reply_user(user_id):
    return redirect(url_for('admin.support_inbox'))