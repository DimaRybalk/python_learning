from database import *
def exit_from_menu():
    exit()

menu = {
    1: (" Показать все книги", get_all_books),
    2: (" Найти книгу по году", get_book_by_year),
    3: (" Удалить книгу", delete_book),
    4: (" Обновить страницы", update_book),
    5: (" Статистика", get_library_stats ),
    0: (" Выход", exit_from_menu)
}

def print_menu():
    for key,value in menu.items():
        print(f"{key}:{value[0]}")

def choose_action(input_name):
    while True:
        try:
            action = int(input(input_name))

            if action not in menu:
                print("Вы должны выбирать только из даных вам опций")
                continue
        
            return action
        
        except ValueError:
            print("Вы должны вводить только числа")



def start_library():
    while True:
        print_menu()
        action = choose_action("Выберите пункт из меню: ")

        func = menu[action][1]

        if action == 1: 
            books = func()
            for b in books:
                print(f"[ID: {b[0]}] Название: {b[1]} | Год: {b[2]}")
            
        elif action == 2: 
            y = int(input("Введите год для поиска: "))
            results = func(y)
            for r in results: print(r)
        
        elif action == 3: 
            book_id = int(input("Введите ID для удаления: "))
            func(book_id)
        
        elif action == 5: 
            stats = func()
            if stats:
                print(f"\nСтатистика: Книг - {stats['total_books']}, Страниц - {stats['total_pages']}")
        elif action == 0:
            exit_from_menu()

start_library()