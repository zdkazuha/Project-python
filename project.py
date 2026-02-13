import os;
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'user_data.json')

def main():
    database = load_database()
    while True:
        try:
            print('''
1 - Заповнення бази даних
2 - Перегляд даних про всі товари
3 - Доповнення бази даних товаром
4 - Видалення товару із бази даних
5 - Редагування запису про певний товар
6 - Упорядкування по полях: назва товару, ціна товару
7 - Пошук: фірма або назва товару
8 - Вибірка: товари певного типу за ціною від Х до У; середня ціна на товари певного типу
9 - Корекція: зміна ціни на товари вказаного типу
10 - Табличний звіт: інформація про телевізори (марка, ціна, назва), впорядкування по полю "назва"
''')
            a = int(input('Введіть номер операції (1-10): '))
            if a < 1 or a > 10:
                print("Будь ласка, введіть номер від 1 до 10.")
                continue
        except ValueError:
            print("Будь ласка, введіть дійсне число.")
            continue
        
        if a == 1:
            database = fill_database(database)
        elif a == 2:
            view_all_products(database)
        elif a == 3:
            database = add_product(database)
        elif a == 4:
            database = delete_product(database)
        elif a == 5:
            database = edit_product(database)
        elif a == 6:
            sort_products(database)
        elif a == 7:
            search_products(database)
        elif a == 8:
            filter_products(database)
        elif a == 9:
            database = correct_price(database)
        elif a == 10:
            generate_report(database)
        else:
            print("Невідома команда. Спробуйте ще раз.")
        
        save_database(database)

def load_database():
    try:
        with open(DB_PATH, 'r') as file:
            return json.load(file)
    except Exception ():
        return {'product': []}

def save_database(database):
    with open(DB_PATH, 'w') as file:
        json.dump(database, file)

def fill_database(database):
    while True:
        type_product = input('Введіть тип продукту: ')
        name = input('Введіть назву товару: ')
        brand = input('Введіть бренд товару: ')
        
        try:
            price = float(input('Введіть ціну товару: '))
            if price <= 0:
                print("Ціна повинна бути більше 0 грн. Спробуйте ще раз.")
                continue
        except ValueError:
            print("Будь ласка, введіть правильну числову ціну.")
            continue
        
        product = {'type': type_product, 'name': name, 'brand': brand, 'price': price}
        database['product'].append(product)

        more = input("Додати ще один товар? (y/n): ")
        if more.lower() != 'y':
            break
    
    return database

def add_product(database):
    return fill_database(database)

def view_all_products(database):
    if not database['product']:
        print("База даних порожня.")
    else:
        for product in database['product']:
            print(f"Тип: {product['type']}, Назва: {product['name']}, Бренд: {product['brand']}, Ціна: {product['price']}")

def delete_product(database):
    if not database['product']:
        print("База даних порожня.")
    else:
        name_to_delete = input('Введіть назву товару для видалення: ')
        found = False
        for product in database['product']:
            if product['name'].lower() == name_to_delete.lower():
                database['product'].remove(product)
                found = True
                print(f"Товар '{name_to_delete}' видалений.")
                break
        
        if not found:
            print(f"Товар з назвою '{name_to_delete}' не знайдено.")
    
    return database

def edit_product(database):
    name_to_edit = input('Введіть назву товару для редагування: ')
    found = False
    for product in database['product']:
        if product['name'].lower() == name_to_edit.lower():
            print("Введіть нові дані (залиште порожнім, якщо не хочете змінювати):")
            new_name = input(f"Нова назва ({product['name']}): ") or product['name']
            new_brand = input(f"Новий бренд ({product['brand']}): ") or product['brand']
            try:
                new_price = input(f"Нова ціна ({product['price']}): ")
                if new_price:
                    new_price = float(new_price)
                    if new_price <= 0:
                        print("Ціна повинна бути більше 0 грн.")
                        return database
                    product['price'] = new_price
            except ValueError:
                print("Неправильне введення ціни.")
                return database
            product['name'] = new_name
            product['brand'] = new_brand
            found = True
            print(f"Товар '{name_to_edit}' успішно оновлений.")
            break
    
    if not found:
        print(f"Товар з назвою '{name_to_edit}' не знайдено.")
    
    return database

def sort_products(database):
    field = input("Сортувати по 'name' або 'price': ").lower()
    if field == 'name':
        sorted_database = sorted(database['product'], key=lambda x: x['name'].lower())
    elif field == 'price':
        sorted_database = sorted(database['product'], key=lambda x: x['price'])
    else:
        print("Неправильне поле для сортування.")
        return
    
    for product in sorted_database:
        print(f"Тип: {product['type']}, Назва: {product['name']}, Бренд: {product['brand']}, Ціна: {product['price']}")

def search_products(database):
    keyword = input("Введіть назву товару або фірму для пошуку: ").lower()
    found = False
    for product in database['product']:
        if keyword in product['brand'].lower() or keyword in product['name'].lower():
            print(f"Тип: {product['type']}, Назва: {product['name']}, Бренд: {product['brand']}, Ціна: {product['price']}")
            found = True
    if not found:
        print(f"Не знайдено товарів за запитом '{keyword}'.")

def filter_products(database):
    product_type = input("Введіть тип товару: ").lower()
    try:
        min_price = float(input("Введіть мінімальну ціну: "))
        max_price = float(input("Введіть максимальну ціну: "))
    except ValueError:
        print("Будь ласка, введіть правильну числову ціну.")
        return
    
    filtered_products = [product for product in database['product'] if product['type'].lower() == product_type and min_price <= product['price'] <= max_price]
    if filtered_products:
        for product in filtered_products:
            print(f"Тип: {product['type']}, Назва: {product['name']}, Бренд: {product['brand']}, Ціна: {product['price']}")
        avg_price = sum(p['price'] for p in filtered_products) / len(filtered_products)
        print(f"Середня ціна для {product_type}: {avg_price:.2f} грн.")
    else:
        print("Не знайдено товарів за заданими критеріями.")

def correct_price(database):
    product_type = input("Введіть тип товару: ").lower()
    try:
        percentage = float(input("Введіть відсоток зміни ціни (наприклад, 5 для збільшення на 5%): "))
    except ValueError:
        print("Будь ласка, введіть правильний відсоток.")
        return database
    
    for product in database['product']:
        if product['type'].lower() == product_type:
            old_price = product['price']
            product['price'] = old_price * (1 + percentage / 100)
            print(f"Ціна товару '{product['name']}' змінена з {old_price} на {product['price']}.")
    
    return database

def generate_report(database):
    sorted_database = sorted(database['product'], key=lambda x: x['name'].lower())
    for product in sorted_database:
        if product['type'].lower() == 'tv':
            print(f"Марка: {product['brand']}, Ціна: {product['price']}, Назва: {product['name']}")

main()
