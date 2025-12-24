# アプリ名: oop2_10_sample
> 図書貸出システムアプリ

概要:
> このアプリでは以下のことができます

> トップ画面で各ページにアクセスと入力されたデータの統計確認ができます。

> ユーザー一覧の確認・新規ユーザの追加

> 本の在庫一覧の確認・在庫の追加

> 現在の貸出状況・新規貸し出し登録

## アピールポイント
>新規ユーザー登録
![libraryapp_newuser](https://github.com/user-attachments/assets/865751af-84c9-4576-aac3-0436cc294459)

>新規ブック登録
![libraryapp_newbook](https://github.com/user-attachments/assets/af7de8c0-194c-4af0-b105-a09615688188)

>新規貸出
![libraryapp_newrent](https://github.com/user-attachments/assets/81e840b5-41e0-4210-9d4c-05e4bc76cbcc)
登録されてるユーザー、本を選ぶだけだからわかりやすい。貸出日もカレンダーから選ぶだけ。

>ダッシュボード
![libraryapp_tukaikata](https://github.com/user-attachments/assets/7cd9d339-a456-47e7-86e9-7d2c494f7b05)
総ユーザー数、総蔵書数、累計貸出数、ジャンル分布、月別貸出推移が一目でわかる。


この部分に、発表に替わる内容を書きます。
アプリケーション動作のサンプル動画などを貼り付けられると良いです。
※動画の貼り付けは、GIFアニメーションなどでも可です。

## 動作条件: require

> 動作に必要な条件を書いてください。

```bash
python 3.13 or higher

# python lib
Flask==3.0.3
peewee==3.17.7
```

## 使い方: usage

> このリポジトリのアプリを動作させるために行う手順を詳細に書いてください。

```bash
$ python app.py
# Try accessing "http://localhost:8080" in your browser.
```
