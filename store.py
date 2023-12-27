import sqlite3

class Store:
    def __init__(self, db_name = 'Microsoft.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        self.conn.commit()

        self.cursor.execute('DELETE FROM products')
        self.conn.commit()

        self.cursor.execute('DELETE FROM sqlite_sequence WHERE name="products"')
        self.conn.commit()

        self.cursor.executemany('INSERT INTO products (name, price) VALUES (?, ?)', [
            ('XBOX Series S', 349.99),
            ('XBOX Series X', 399.99),
            ('Xbox Series X Console Wraps', 49.99),
            ('Xbox Wireless Controller', 45.99),
        ])
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS shopping_cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        ''')
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                address TEXT,
                total_amount REAL,
                order_number INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        self.conn.commit()

    def close_connection(self):
        self.conn.close()