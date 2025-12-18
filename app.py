from flask import Flask, render_template
from models import initialize_database
from models.db import db
from routes import blueprints

app = Flask(__name__)

# データベースの初期化
initialize_database()

# --- 修正箇所: 安全な接続管理 ---
@app.before_request
def before_request():
    # 「もし接続が閉じていたら」つなぐ、という書き方に変更
    if db.is_closed():
        db.connect()

@app.teardown_request
def _db_close(exc):
    # 「もし接続が開いていたら」閉じる
    if not db.is_closed():
        db.close()
# -----------------------------

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)