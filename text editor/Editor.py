import os

def open_or_create():

    filename = input("Please enter the filename you want to open or create: ")
    exit_word = "SAVE"
    mode = "w"

    if os.path.exists(filename):
        print(f"{filename} found. Opening file.")
        while True:
            choice = input("Do you want to (o)verwrite or (a)ppend? (o/a): ").lower()
            if choice in ["o", "a"]:
                if choice == "a":
                    mode = "a"
                break
            else:
                print("You need to choose only from o/a options")         
    else:
        print(f"{filename} not found. Creating a new file.")
        
    with open(filename, mode) as f:
        print("\n")
        print("Enter your text (type 'SAVE' on a new line to save and exit): ")
        while True:
            line = input()
            if line == exit_word:
                print(f"File {filename} saved.")
                break
            f.write(line + "\n") 

def replace():
    replacement = input("Where do you want to make replacement?: ")
    if os.path.exists(replacement):
        with open(replacement, "r") as f:
            content = f.read()
            
            if not content:
                print("File is empty.")
                return

            print("\n--- Current Content ---")
            print(content)

            searching_word = input("What word do you want to find?: ")
            if searching_word in content:
                replace_word = input("Write new content: ")
                new_content = content.replace(searching_word,replace_word)
                with open(replacement, "w") as f:
                    f.write(new_content)
                    print(f"All changes saved to {replacement}.")
            else:
                print(f"There are no such words as {searching_word}")
    else:
        print(f"There are no file with such name as {replacement}")

def exit_button():
    exit()

menu = {
    1: ("open or create", open_or_create),
    2: ("find and replace", replace),
    3: ("Exit", exit_button)
}

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

def show_menu():
    for key,value in menu.items():
        print(f"{key}: {value[0].capitalize()}")

def start_work():
    print("-"*15)
    print("Simple Text Editor Menu: ")
    show_menu()
    user_choice = choice_validator("Enter your choice: ")
    starting_task(user_choice)

while True:
    start_work()

