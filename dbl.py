import sqlite3

def display_db():
    conn = sqlite3.connect('amazon_products.db')
    c = conn.cursor()

    c.execute("SELECT * FROM products")
    rows = c.fetchall()

    for row in rows:
        print(row[0])  # 商品名の表示

    conn.close()

if __name__ == '__main__':
    display_db()
