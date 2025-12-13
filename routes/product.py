from flask import Blueprint, render_template, request, redirect, url_for
from models import Product

# Blueprintの作成
product_bp = Blueprint('product', __name__, url_prefix='/products')


@product_bp.route('/')
def list():
    products = Product.select()
    return render_template('product_list.html', title='本データ一覧', items=products)


@product_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        maxNumber = int(request.form['maxNumber'])
        currentNumber = int(request.form['currentNumber'])

        Product.create(
            title = title,
            genre = genre,
            maxNumber = maxNumber,
            currentNumber = currentNumber
        )
        return redirect(url_for('product.list'))
    
    return render_template('product_add.html')


@product_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit(product_id):
    product = Product.get_or_none(Product.id == product_id)
    if not product:
        return redirect(url_for('product.list'))

    if request.method == 'POST':
        product.title = request.form['title']
        product.genre = request.form['genre']
        product.maxNumber = int(request.form['maxNumber'])
        product.currentNumber = int(request.form['currentNumber'])
        product.save()
        return redirect(url_for('product.list'))

    return render_template('product_edit.html', product=product)