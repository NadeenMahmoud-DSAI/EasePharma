import os
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from app.models.product_model import ProductModel
from app.models.order_model import OrderModel
from app.models.message_model import MessageModel

product_bp = Blueprint('product', __name__)

def get_data_path():
    return current_app.config['DATA_PATH']

@product_bp.route('/')
def home():
    products = ProductModel.get_all(get_data_path(), limit=12)
    return render_template('customer/home.html', products=products)

@product_bp.route('/search')
def search():
    query = request.args.get('q', '')
    results = ProductModel.search(get_data_path(), query) if query else []
    return render_template('customer/home.html', products=results)

@product_bp.route('/add_to_cart/<int:id>', methods=['POST'])
def add_to_cart(id):
    if 'cart' not in session: session['cart'] = {}
    cart = session['cart']
    cart[str(id)] = cart.get(str(id), 0) + 1
    session.modified = True
    flash("Item added to cart!")
    return redirect(request.referrer or url_for('product.home'))

@product_bp.route('/cart')
def cart_view():
    data_path = get_data_path()
    cart = session.get('cart', {})
    items = []
    total = 0.0
    for pid, qty in cart.items():
        p = ProductModel.get_by_id(data_path, int(pid))
        if p:
            sub = p.price * qty
            total += sub
            items.append({'product': p, 'qty': qty, 'subtotal': sub})
    return render_template('customer/cart.html', items=items, total=total)

@product_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        cart = session.get('cart', {})
        if not cart: return redirect(url_for('product.home'))
        
        OrderModel.create_from_cart(get_data_path(), session['user_id'], cart)
        session.pop('cart', None)
        flash("Order placed successfully!")
        return redirect(url_for('product.order_history'))
        
    return render_template('customer/checkout.html')

@product_bp.route('/orders')
def order_history():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    orders = OrderModel.get_by_user(get_data_path(), session['user_id'])
    return render_template('customer/order_history.html', orders=orders)

# ORDER TRACKING
@product_bp.route('/track/<order_id>')
def track_order(order_id):
    if 'user_id' not in session: 
        return redirect(url_for('auth.login'))
    data_path = get_data_path()
    orders = OrderModel.get_all(data_path)
    order = next((o for o in orders if str(o.order_id) == str(order_id)), None)
    
    if not order:
        flash("Order not found.")
        return redirect(url_for('product.order_history'))
        
    return render_template('customer/track_order.html', order=order)

#SUPPORT ROUTE
@product_bp.route('/support', methods=['GET', 'POST'])
def customer_support():
    if 'user_id' not in session: 
        return redirect(url_for('auth.login'))
    
    data_path = get_data_path()
    user_id = session['user_id']
    
    if request.method == 'POST':
        msg = request.form.get('message')
        if msg:
            MessageModel.send_message(data_path, user_id, 'Customer', msg)
        return redirect(url_for('product.customer_support'))
        
    messages = MessageModel.get_conversation(data_path, user_id)
    return render_template('customer/support.html', messages=messages)