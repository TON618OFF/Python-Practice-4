import random
import bcrypt

class User:
    def __init__(self, store):
        self.store = store
        self.authenticated_user = None

    def validate_credentials(self, login, password):
        if not login.strip() or not password.strip():
            print("-------------------------------------------------------------------\nЛогин и пароль не могут быть пустыми. Пожалуйста, попробуйте снова.\n-------------------------------------------------------------------")
            return False
        return True

    def authenticate(self, login, password):
        if not self.validate_credentials(login, password):
            return False

        self.store.cursor.execute('SELECT * FROM users WHERE login = ?', (login,))
        existing_user = self.store.cursor()

        if existing_user and bcrypt.checkpw(password.encode('utf-8'), existing_user[2]):
            self.authenticated_user = existing_user
            return True
        else:
            print("------------------------------------------------------------\nНеправильный логин или пароль. Пожалуйста, попробуйте снова.\n------------------------------------------------------------")
            return False

    def display_products(self):
        self.store.cursor.execute('SELECT * FROM products')
        products = self.store.cursor.fetchall()
        print("----------------\nТовары в Microsoft\n----------------")
        for product in products:
            print(f"{product[0]}. {product[1]} - ${product[2]}")
        return products

    def add_to_cart(self, product_id):
        self.store.cursor.execute('INSERT INTO shopping_cart (user_id, product_id) VALUES (?, ?)',
                                  (self.authenticated_user[0], product_id))
        self.store.conn.commit()

class Client(User):
    def __init__(self, store):
        super().__init__(store)

    def validate_product_id(self, product_id, products):
        try:
            product_id = int(product_id)
            if not (1 <= product_id <= len(products)):
                print(
                    "----------------------------------------------------\nНеверный номер товара.\n----------------------------------------------------")
                return False
            return True
        except ValueError:
            print(
                "-----------------------------------------\nНеверный ввод.\n-----------------------------------------")
            return False

    def add_to_cart(self, product_id):
        products = self.display_products()
        if not self.validate_product_id(product_id, products):
            return

        self.store.cursor.execute('INSERT INTO shopping_cart (user_id, product_id) VALUES (?, ?)',
                                  (self.authenticated_user[0], product_id))
        self.store.conn.commit()

    def display_cart(self):
        self.store.cursor.execute('''
            SELECT products.name, products.price
            FROM shopping_cart
            JOIN products ON shopping_cart.product_id = products.id
            WHERE shopping_cart.user_id = ?
        ''', (self.authenticated_user[0],))
        cart_items = self.store.cursor.fetchall()

        def display_products(self):
            return super(().display_products())

        if cart_items:
            total_sum = sum(item[1] for item in cart_items)
            print("------------------------\nТовары в корзине:\n------------------------")
            for item in cart_items:
                print(f"{item[0]} - ${item[1]}")
            print(f"--------------------------\nСумма: ${total_sum}")
        else:
            print("----------------------------\nКорзина пуста.\n----------------------------")

    def checkout(self, address):
        self.store.cursor.execute('''
            SELECT products.price
            FROM shopping_cart
            JOIN products ON shopping_cart.product_id = products.id
            WHERE shopping_cart.user_id = ?
        ''', (self.authenticated_user[0],))
        prices = self.store.cursor.fetchall()
        total_sum = sum(price[0] for price in prices)

        self.store.cursor.execute('''
            INSERT INTO orders (user_id, address, total_amount, order_number)
            VALUES (?, ?, ?, ?)
        ''', (self.authenticated_user[0], address, total_sum))
        self.store.conn.commit()

        self.store.cursor.execute('DELETE FROM shopping_cart WHERE user_id = ?', (self.authenticated_user[0],))
        self.store.conn.commit()

        print("\nЗаказ оформлен!")
        print(f"Номер заказа №{order_number}")
        print("--------------------")
        print(f"Итого: ${total_sum}")

class Administrator(User):
    ADMIN_USERNAME = "Administrator2024"
    ADMIN_PASSWORD = "2_0_2_4"

    def authenticate(self, login, password):
        return login == self.ADMIN_USERNAME and password == self.ADMIN_PASSWORD

    def add_product(self, name, price):
        self.store.cursor.execute('INSERT INTO products (name, price) VALUES (?, ?)', (name, price))
        self.store.conn.commit()

    def remove_product(self, name):
        self.store.cursor.execute('DELETE FROM products WHERE name = ?', (name,))
        self.store.conn.commit()

    def change_product_name(self, current_name, new_name):
        self.store.cursor.execute('UPDATE products SET name = ? WHERE name = ?', (new_name, current_name))
        self.store.conn.commit()