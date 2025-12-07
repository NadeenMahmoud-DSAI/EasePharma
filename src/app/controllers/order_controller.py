from flask import (
    Blueprint, current_app, render_template, request,
    redirect, url_for, flash, session
)
import os
import csv
from datetime import datetime

from app.models.product_model import ProductModel

order_bp = Blueprint(
    "order",
    __name__,
    template_folder="../views/templates",
    static_folder="../views/static"
)

ORDERS_FILE = "orders.csv"
FIELDNAMES = ["order_id", "user_email", "total", "items", "timestamp"]


#  utility functions
def get_orders_csv_path():
    data_dir = current_app.config.get("DATA_PATH")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, ORDERS_FILE)


def write_order(user_email: str, total: float, items: list):
    path = get_orders_csv_path()

    # Load existing orders
    existing = []
    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            existing = list(reader)

    numeric_ids = [int(o["order_id"]) for o in existing if o["order_id"].isdigit()]
    new_id = str(max(numeric_ids) + 1) if numeric_ids else "1"

    order_row = {
        "order_id": new_id,
        "user_email": user_email,
        "total": f"{total:.2f}",
        "items": str(items),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Write back
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for o in existing:
            writer.writerow(o)
        writer.writerow(order_row)

    return new_id


#  CHECKOUT PAGE
@order_bp.route("/checkout")
def checkout():
    cart = session.get("cart", {})
    if not cart:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("product.home"))

    data_dir = current_app.config.get("DATA_PATH")
    items = []
    total = 0

    for pid, qty in cart.items():
        product = ProductModel.find_by_id(data_dir, pid)
        if not product:
            continue
        subtotal = product.final_price * int(qty)
        total += subtotal
        items.append({
            "product": product,
            "qty": int(qty),
            "subtotal": subtotal
        })

    return render_template(
        "customer/checkout.html",
        items=items,
        total=round(total, 2)
    )


#  PLACE ORDER
@order_bp.route("/place_order", methods=["POST"])
def place_order():
    cart = session.get("cart", {})
    if not cart:
        flash("Cart is empty.", "danger")
        return redirect(url_for("product.home"))

    user_email = session.get("user_email", None)
    if not user_email:
        flash("You must be logged in to place an order.", "danger")
        return redirect(url_for("auth.login"))

    data_dir = current_app.config.get("DATA_PATH")
    items = []
    total = 0

    # Build order summary
    for pid, qty in cart.items():
        p = ProductModel.find_by_id(data_dir, pid)
        if not p:
            continue
        subtotal = p.final_price * int(qty)
        total += subtotal
        items.append({
            "id": p.id,
            "name": p.name,
            "qty": int(qty),
            "subtotal": round(subtotal, 2)
        })

    # Save order
    order_id = write_order(user_email, total, items)

    # Clear cart
    session["cart"] = {}

    flash(f"Order placed successfully! Order ID: {order_id}", "success")
    return redirect(url_for("order.order_confirmation", order_id=order_id))


#  ORDER CONFIRMATION 
@order_bp.route("/order_confirmation/<order_id>")
def order_confirmation(order_id):
    return render_template(
        "customer/order_confirmation.html",
        order_id=order_id
    )


#  ORDER HISTORY 
@order_bp.route("/order_history")
def order_history():
    user_email = session.get("user_email", None)
    if not user_email:
        flash("You must be logged in to view orders.", "danger")
        return redirect(url_for("auth.login"))

    path = get_orders_csv_path()
    history = []

    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["user_email"] == user_email:
                    history.append(row)

    return render_template(
        "customer/order_history.html",
        orders=history
    )
