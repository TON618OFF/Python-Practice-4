import bcrypt

from store import Store
from user import Client, Administrator

store = Store()

while True:
    print("-----------------------------------------------Добро пожаловать в ИС Microsoft!-----------------------------------------------\n")

    print("1. Авторизоваться")
    print("2. Зарегистрироваться")
    print("3. Выйти")
    choice = input("\nВыберите действие: ")

    if choice == '1':
        print("------------\nАвторизация\n------------")
        print("1. Войти как клиент")
        print("2. Войти как сотрудник")
        print("3. Обратно")
        auth_choice = input("\nВыберите действие: ")

        if auth_choice == '1':
            client = Client(store)

            while True:
                login_client = input("\nЛогин: ")
                password_client = input("Пароль: ")

                if login_client.strip() and password_client.strip():
                    break
                else:
                    print("-----------------------------------------------\nЛогин и пароль не могут быть пустыми. Пожалуйста, попробуйте снова.\n-----------------------------------------------")

            if client.authenticate(login_client, password_client):
                print("\nВход успешен!")
            else:
                continue

            while True:
                print("-----------------------------------------------\nВы вошли в Microsoft!\n-----------------------------------------------")
                print("1. Товары")
                print("2. Корзина")
                print("3. Выйти")

                client_action = input("\nВыберите действие: ")

                if client_action == '1':
                    client.display_products()
                    add_to_cart = input("\nУкажите номер товара для добавления в корзину: ")

                    try:
                        product_id = int(add_to_cart)
                        products = client.display_products()
                        if 1 <= product_id <= len(products):
                            client.add_to_cart(product_id)
                            print(f"-----------------------------------------------\nТовар '{products[product_id - 1][1]}' добавлен.\n-----------------------------------------------")
                        else:
                            print("-----------------------------------------------\nНеверный номер товара.\n-----------------------------------------------")
                    except ValueError:
                        print("-----------------------------------------------\nНеверный ввод.\n-----------------------------------------------")

                elif client_action == '2':
                    client.display_cart()

                    print("1. Оформить заказ")
                    print("2. Вернуться назад")
                    cart_choice = input("\nВыберите действие: ")

                    if cart_choice == '1':
                        print("-----------------\nОФОРМЛЕНИЕ ЗАКАЗА\n-----------------")

                        address = input("\nВведите адрес: ")
                        client.checkout(address)
                        break

                    elif cart_choice == '2':
                        continue

                elif client_action == '3':
                    print("-----------------------------------------\nДо встречи!\n-----------------------------------------")
                    break

        elif auth_choice == '2':
            administrator = Administrator(store)

            while True:
                administrator_login = input("\nЛогин: ")
                administrator_password = input("Пароль: ")

                if administrator_login.strip() and administrator_password.strip():
                    break
                else:
                    print("-----------------------------------------\nЗначение полей не может быть пустым.\n-----------------------------------------")

            if administrator.authenticate(administrator_login, administrator_password):
                print("\nВход успешен!")

                while True:
                    print("------------------------------------\nКакие изменения внести в Microsoft?\n------------------------------------")
                    print("\n1. Добавить товар")
                    print("2. Удалить товар")
                    print("3. Переименовать товара")
                    print("4. Выйти")

                    administrator_action = input("\nВыберите действие: ")

                    if administrator_action == '1':
                        print("-----------------\nДобавление товара...\n-----------------")
                        while True:
                            product_name = input("\nВведите название товара: ")
                            product_price = input("Введите цену товара: ")
                            try:
                                product_price = float(product_price)
                                if product_name.strip() and product_price >= 0:
                                    administrator.add_product(product_name, product_price)
                                    print(f"-----------------------------------------\nТовар '{product_name}' добавлен!\n-----------------------------------------")
                                    break
                                else:
                                    print("-----------------------------------------\nНазвание товара не может быть пустым.\n-----------------------------------------")
                            except ValueError:
                                print("-----------------------------------------\nНеверный формат цены. Пожалуйста, введите число.\n-----------------------------------------")

                    elif administrator_action == '2':
                        print("--------------------------\nУдаления товара...\n--------------------------")
                        while True:
                            product_name_to_delete = input("\nВведите имя товара для удаления: ")

                            administrator.remove_product(product_name_to_delete)
                            print(f"-----------------------------------------\nТовар '{product_name_to_delete}' успешно удален.\n-----------------------------------------")
                            break

                    elif administrator_action == '3':
                        print("--------------------------\nИзменения названия товара...\n--------------------------")
                        while True:
                            product_name_to_change = input("\nВведите название товара для изменения: ")

                            new_product_name = input("Введите новое название товара: ")
                            administrator.change_product_name(product_name_to_change, new_product_name)
                            print(f"-----------------------------------------\nНазвание товара изменено на '{new_product_name}'.\n-----------------------------------------")
                            break

                    elif administrator_action == '4':
                        print("-----------------\nДо встречи!\n-----------------")
                        break
            else:
                print("-----------------------------------------\nНеверный логин или пароль. Пожалуйста, попробуйте снова.\n-----------------------------------------")

    elif choice == '2':
        print("-----------\nРЕГИСТРАЦИЯ\n-----------")
        print("Введите не менее 6 символов")

        while True:
            login_client = input("\nПридумайте логин: ")

            if len(login_client) >= 6:
                break
            else:
                print("-----------------------------------------\nЛогин должен содержать не менее 6 символов и не должен быть пустым.\n-----------------------------------------")

        while True:
            password_client = input("Придумайте пароль (Должен содержать не менее 8 символов): ")

            if len(password_client) >= 8:
                break
            else:
                print("-----------------------------------------\nПароль не может быть пустым.\n-----------------------------------------")

        store.cursor.execute('SELECT * FROM users WHERE login = ?', (login_client,))
        existing_user = store.cursor.fetchone()

        if existing_user:
            print("-------------------------------------------------------------------------------\nПользователь с таким логином уже существует. Пожалуйста, выберите другой логин.\n-------------------------------------------------------------------------------")


        else:

            hashed_password = bcrypt.hashpw(password_client.encode('utf-8'), bcrypt.gensalt())

            store.cursor.execute('INSERT INTO users (login, password) VALUES (?, ?)', (login_client, hashed_password))

            store.conn.commit()

            print("\nРегистрация завершена!")

    elif choice == '3':
        print("----------------------------\nВы вышли из Microsoft!\n----------------------------")
        break

    else:
        print("----------------------------\nНеправильный ввод.\n----------------------------")

store.close_connection()