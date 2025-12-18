from flask import Flask, render_template
from models import initialize_database
from routes import blueprints

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
    # --- 1. KPI (基本統計) ---
    user_count = User.select().count()
    product_count = Product.select().count()
    order_count = Order.select().count()

    # --- 2. ジャンル分布 (円グラフ用) ---
    genre_query = (Product
                   .select(Product.genre, fn.COUNT(Product.id).alias('count'))
                   .group_by(Product.genre))
    
    # Chart.js用にリストに変換
    genre_labels = [item.genre for item in genre_query]
    genre_data = [item.count for item in genre_query]

    # --- 3. 月毎の貸出数 (折れ線グラフ用) ---
    monthly_query = (Order
                     .select(fn.strftime('%Y-%m', Order.order_date).alias('month'),
                             fn.COUNT(Order.id).alias('count'))
                     .group_by(fn.strftime('%Y-%m', Order.order_date))
                     .order_by(fn.strftime('%Y-%m', Order.order_date)))
    
    # Chart.js用にリストに変換
    month_labels = [item.month for item in monthly_query]
    month_data = [item.count for item in monthly_query]

    return render_template('index.html',
                           user_count=user_count,
                           product_count=product_count,
                           order_count=order_count,
                           genre_labels=genre_labels,
                           genre_data=genre_data,
                           month_labels=month_labels,
                           month_data=month_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
