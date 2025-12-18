from flask import Blueprint, render_template, request, redirect, url_for
from models import Order, User, Product
# 日付計算用に timedelta を追加
from datetime import datetime, timedelta

order_bp = Blueprint('order', __name__, url_prefix='/orders')


@order_bp.route('/')
def list():
    orders = Order.select()
    # テンプレート側で日付計算ができるように timedelta を渡す
    return render_template('order_list.html', title='注文一覧', items=orders, timedelta=timedelta)


@order_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        product_id = request.form.get('product_id')
        
        if not user_id or not product_id:
            return redirect(url_for('order.add'))

        user = User.get_or_none(User.id == int(user_id))
        product = Product.get_or_none(Product.id == int(product_id))

        if not user or not product:
            return redirect(url_for('order.add'))

        # --- 在庫管理ロジック ---
        if product.currentNumber <= 0:
            # 本来はエラーメッセージを出すべきですが、簡易的に一覧へ戻します
            return redirect(url_for('order.list'))
        
        # 在庫を1つ減らして保存
        product.currentNumber -= 1
        product.save()
        # ---------------------

        Order.create(user=user, product=product, order_date=datetime.now())
        return redirect(url_for('order.list'))
    
    users = User.select()
    products = Product.select()
    return render_template('order_add.html', users=users, products=products)


@order_bp.route('/edit/<int:order_id>', methods=['GET', 'POST'])
def edit(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect(url_for('order.list'))

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        product_id = request.form.get('product_id')

        # ユーザー変更
        if user_id:
            user = User.get_or_none(User.id == int(user_id))
            if user:
                order.user = user

        # 本の変更
        if product_id:
            product = Product.get_or_none(Product.id == int(product_id))
            if product:
                order.product = product

        order.save()
        return redirect(url_for('order.list'))

    users = User.select()
    products = Product.select()
    return render_template('order_edit.html', order=order, users=users, products=products)