from datetime import datetime

from repositories.user_repository import UserRepository
from repositories.category_repository import CategoryRepository
from repositories.transaction_repository import TransactionsRepository

from models.user import User
from models.category import Category
from models.transaction import Transaction

# CHAT GPT писал этот код для проверки взаимодействия с БД!!!!

user_repo = UserRepository()
category_repo = CategoryRepository()
transaction_repo = TransactionsRepository()


def get_int_input(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Введите число!")


def get_float_input(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Введите корректную сумму!")


def create_user():

    email = input("Email: ").strip()
    password = input("Password: ").strip()

    if not email or not password:
        print("Email и пароль не могут быть пустыми")
        return

    user = User(
        id=None,
        email=email,
        password=password,
        created_at=str(datetime.now())
    )

    try:
        user_repo.create_user(user)
        print("Пользователь создан")
    except Exception as e:
        print("Ошибка при создании пользователя:", e)


def create_category():

    name = input("Название категории: ").strip()
    type_ = input("Тип (income/expense): ").strip().lower()

    if not name:
        print("Название не может быть пустым")
        return

    if type_ not in ["income", "expense"]:
        print("Тип должен быть income или expense")
        return

    category = Category(None, name, type_)

    try:
        category_repo.create_category(category)
        print("Категория создана")
    except Exception as e:
        print("Ошибка при создании категории:", e)


def add_transaction():

    email = input("Email пользователя: ").strip()
    user = user_repo.get_user_by_email(email)

    if not user:
        print("Пользователь не найден")
        return

    categories = category_repo.get_all_categories()

    if not categories:
        print("Нет категорий. Сначала создайте категорию.")
        return

    print("\nДоступные категории:")
    for c in categories:
        print(f"id: {c[0]} | name: {c[1]} | type: {c[2]}")

    category_id = get_int_input("Введите id категории: ")

    category_exists = any(c[0] == category_id for c in categories)

    if not category_exists:
        print("Категория не существует")
        return

    amount = get_float_input("Сумма: ")

    if amount <= 0:
        print("Сумма должна быть больше 0")
        return

    description = input("Описание: ").strip()

    transaction = Transaction(
        id=None,
        user_id=user[0],
        category_id=category_id,
        amount=amount,
        date=datetime.now(),
        descriptions=description,
        created_at=str(datetime.now())
    )

    try:
        transaction_repo.create_transaction(transaction)
        print("Транзакция добавлена")
    except Exception as e:
        print("Ошибка при добавлении транзакции:", e)


def show_transactions():

    email = input("Email пользователя: ").strip()
    user = user_repo.get_user_by_email(email)

    if not user:
        print("Пользователь не найден")
        return

    try:
        transactions = transaction_repo.get_transaction_by_user(user[0])

        if not transactions:
            print("Транзакций нет")
            return

        print("\nТранзакции:")
        for t in transactions:
            print(t)

    except Exception as e:
        print("Ошибка при получении транзакций:", e)


def show_balance():

    email = input("Email пользователя: ").strip()
    user = user_repo.get_user_by_email(email)

    if not user:
        print("Пользователь не найден")
        return

    try:
        totals = transaction_repo.get_totals(user[0])

        if not totals:
            print("Нет данных")
            return

        print("\nФинансы:")
        print("Доход:", totals.get("income", 0))
        print("Расход:", totals.get("expense", 0))
        print("Баланс:", totals.get("balance", 0))

    except Exception as e:
        print("Ошибка при получении статистики:", e)


def menu():

    while True:

        print("\n====== FINANCE TRACKER ======")
        print("1. Создать пользователя")
        print("2. Создать категорию")
        print("3. Добавить транзакцию")
        print("4. Показать транзакции")
        print("5. Показать баланс")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        try:

            if choice == "1":
                create_user()

            elif choice == "2":
                create_category()

            elif choice == "3":
                add_transaction()

            elif choice == "4":
                show_transactions()

            elif choice == "5":
                show_balance()

            elif choice == "0":
                print("Выход...")
                break

            else:
                print("Неверный пункт меню")

        except Exception as e:
            print("Произошла ошибка:", e)


if __name__ == "__main__":
    menu()