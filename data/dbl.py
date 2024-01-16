import sqlite3
import pandas as pd

def save_category_to_db(category):
    # CSVファイルとデータベースファイルのパス
    file_path = f'/Users/cider/Desktop/dsproen/local/{category}.csv'
    database_file = f'/Users/cider/Desktop/dsproen/local/{category}.db'

    # データベースに接続
    conn = sqlite3.connect(database_file)

    # CSVファイルを読み込み
    df = pd.read_csv(file_path)
    df.columns = ['title']

    # データベースにデータを保存
    df.to_sql('amazon_products', conn, if_exists='replace', index=False)

    # 接続を閉じる
    conn.close()

# 例として 'mystery' カテゴリを保存
save_category_to_db('mystery')
