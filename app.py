from flask import Flask, render_template
from models import initialize_database, User, Product, Order # User, Product, Orderを追加
from models.db import db
from routes import blueprints
from collections import defaultdict # 集計用にインポート

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 安全な接続管理
@app.before_request
def before_request():
    if db.is_closed():
        db.connect()

@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()

# 各Blueprintを登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)


# --- ホームページ（ダッシュボード化） ---
@app.route('/')
def index():
    # 1. 基本データの集計
    user_count = User.select().count()
    
    # 在庫の総数は、全商品のcurrentNumberを合計する
    total_stock = 0
    products = Product.select()
    for p in products:
        total_stock += p.currentNumber

    # 2. グラフ用データの集計
    # 注文データを全件取得（商品情報も一緒に持ってくる）
    orders = Order.select().join(Product)

    # A. ジャンルごとの貸出数（円グラフ用）
    genre_counts = defaultdict(int)
    # B. 月ごとの貸出数（棒グラフ用）
    monthly_counts = defaultdict(int)

    for order in orders:
        # ジャンル集計
        genre_counts[order.product.genre] += 1
        
        # 月別集計 (例: "2024-12" のようなキーを作る)
        month_key = order.order_date.strftime('%Y-%m')
        monthly_counts[month_key] += 1

    # 辞書データをリストや並び替え済みの形に整理して渡す
    
    # 円グラフデータ
    genre_labels = list(genre_counts.keys())
    genre_data = list(genre_counts.values())

    # 棒グラフデータ（月順に並べる）
    sorted_months = sorted(monthly_counts.keys())
    monthly_data = [monthly_counts[m] for m in sorted_months]

    return render_template(
        'index.html',
        user_count=user_count,
        total_stock=total_stock,
        genre_labels=genre_labels,
        genre_data=genre_data,
        month_labels=sorted_months,
        month_data=monthly_data
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)