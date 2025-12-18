from flask import Blueprint, render_template, request, redirect, url_for
from models import Order, User, Product
from datetime import datetime

order_bp = Blueprint('order', __name__, url_prefix='/orders')


@order_bp.route('/')
def list():
    orders = Order.select()
    return render_template('order_list.html', title='注文一覧', items=orders)


@order_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # 1. 安全に入力値を取得 (main側の記述を採用)
        user_id = request.form.get('user_id')
        product_id = request.form.get('product_id')
        
        # IDが空でないかチェック
        if not user_id or not product_id:
            return redirect(url_for('order.add'))

        # 2. データベースからモデルを取得 (main側の記述を採用)
        user = User.get_or_none(User.id == int(user_id))
        product = Product.get_or_none(Product.id == int(product_id))
        
        # ユーザーや本が存在しない場合のチェック
        if not user or not product:
            return redirect(url_for('order.add'))

        # 3. 在庫チェック (product側の記述を採用)
        if product.currentNumber <= 0:
            # エラー処理（本来は画面にメッセージを出すべきですが、今はリダイレクト）
            return redirect(url_for('order.list'))

        # 4. 貸出処理 (両方の記述を統合)
        Order.create(
            user=user, 
            product=product, 
            order_date=datetime.now()
        )

        # 5. 在庫を減らす (product側の記述を採用)
        product.currentNumber -= 1
        product.save()

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

        if user_id:
            user = User.get_or_none(User.id == int(user_id))
            if user:
                order.user = user

        if product_id:
            product = Product.get_or_none(Product.id == int(product_id))
            if product:
                order.product = product

        order.save()
        return redirect(url_for('order.list'))

    users = User.select()
    products = Product.select()
    return render_template('order_edit.html', order=order, users=users, products=products)