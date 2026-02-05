import time
import json

DATA_FILE = "list.json"

try:
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = []

def animation(text,x,delay):
    print(text, end="", flush=True) 
    for _ in range(x):      
        time.sleep(delay)     
        print(".", end="", flush=True) 
        time.sleep(0.1)
    print()

def view_task():
    animation("Viewing your tasks:",3,0.15)
    if not data:
        print("Your list is empty!")
        return
    counter = 0
    for item in data:
        print("-"*15)
        counter +=1
        print(f"Task# {counter}")
        for key,value in item.items():
            print(f"{key.title()}: {value.title()}")

def save_tasks():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_task():
    category = input("Type category of your task: ")
    description = input("Type your goal: ")
    task = {
        "category": category,
        "description": description,
    }
    data.append(task)
    save_tasks()
    animation("Task was successfully added!",3,0.1)

def remove_task():
    if not data:
        print("No tasks to remove!")
        return
    
    while True:
        try:
            if len(data) == 1:
                index = int(input(f"Which task you want to remove? ({len(data)}): ")) - 1
            else:
                index = int(input(f"Which task you want to remove? (1-{len(data)}): ")) - 1

            if 0 <= index < len(data):
                break
            else:
                print(f"Please enter a number between 1 and {len(data)}")
        except ValueError:
            print("Please enter a valid number")
    
    animation(f"Removing task number {index+1}",3,0.25)
    data.pop(index)
    save_tasks()
    print("Task was successfully removed!")


def exit_button():
    animation("Exiting",3,0.25)
    exit()

menu = {
    1: ("View tasks", view_task),
    2: ("Add a task", add_task),
    3: ("Remove task", remove_task),
    4: ("Exit", exit_button)
}

def show_menu():
    for key,value in menu.items():
        print(f"{key}. {value[0]}")

def choice_validator(prompt):
    choices_list = [choice for choice in menu]
    while True:
        try:
            user_choice = int(input(prompt))
            if user_choice in choices_list:
                return user_choice
            else:
                print("You need to choose only from menu options")
        except ValueError:
                print("Please enter a number")

def starting_task(user_choice):
    menu[user_choice][1]()

def start_work():
    print("-"*15)
    print("Todo List Menu: ")
    show_menu()
    user_choice = choice_validator("Enter your choice: ")
    starting_task(user_choice)

while True:
    start_work()


