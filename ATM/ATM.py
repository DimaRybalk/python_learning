import random

users = []

def check_balance(user):
    print(f"\n--- Account Balance ---")
    print(f"User:{user.ID}, name: {user.name}")
    print(f"Current balance: {user.balance}")

def deposit_money(user):
    while True:
        try:
            deposit_amount = int(input("How many you want to deposit?: "))
            if deposit_amount > 0:
                user.add_to_balance(deposit_amount)
                break
            else:
                print("You need to deposit more than 0")
                continue
        except ValueError:
            print("You need to type only numbers")

def withdraw_money(user):
    while True:
        try:
            withdraw_amount = int(input("How many you want to withdraw?: "))
            if 0 < withdraw_amount <= user.balance:
                user.withdraw(withdraw_amount)
                break

            if withdraw_amount <= 0:
                print("You need to withdraw more than 0")
            elif withdraw_amount > user.balance:
                print(f"You can't withdraw more than {user.balance}")

        except ValueError:
            print("You need to type only numbers")

def account_history(user):
    print(f"\n--- Transaction History for {user.name} with ID: {user.ID} ---")
    if not user.history:
        print("No transactions yet.")
    else:
        for i, item in enumerate(user.history, 1): 
            print(f"{i}. {item}")

def change_PIN(user):
    if user.status == True:
        while user.attempts > 0:
            current_PIN = input("Enter your current PIN: ")
            if current_PIN == user.PIN:
                while True:
                        new_PIN = input("Enter new PIN (4 digits): ")
                        if len(new_PIN) == 4 and new_PIN.isdigit():
                            user.PIN = new_PIN
                            user.history.append("PIN changed")
                            print("PIN successfully changed!")
                            return
                        else:
                            print("Length of PIN must be 4")
            else:
                 user.attempts = user.decrease_attempts()
    else:
        print("Card is blocked!")
        return

def user_info(user):
        print(f"\n--- Full Account Info ---")
        print(f"Name: {user.name}")
        print(f"Account ID: {user.ID}")
        print(f"Current Balance: ${user.balance}")
        print(f"Total transactions made: {len(user.history)}")
        print("-------------------------")

def transfer_money(user):
    search = input("Enter ID of user you want to transfer money: ")
    recipient = find_user(search)
    if recipient:
        if recipient.ID == user.ID:
            print("You cannot transfer money to yourself!")
            return

        while True:
            try:
                number = int(input("How many you want to transfer?: "))
                if 0 < number <= user.balance:
                    user.withdraw(number) 
                    recipient.add_to_balance(number)
                    user.history.append(f"Transfer to {recipient.name} (ID: {recipient.ID}): -${number}")
                    recipient.history.append(f"Transfer from {user.name} (ID: {user.ID}): +${number}")
                    print("Transfer successful!")
                    return
                
                if number <= 0:
                    print("You need to type number more than 0")
                elif number > user.balance:
                    print(f"You can't transfer more than {user.balance}")
            except ValueError:
                print("You need to type only numbers")
    else:
        print(f"There are no users with ID: {search}")


def find_user(entered_ID):
    if not users:
        print("There are no users")
        return None

    for user in users:
        if str(user.ID) == str(entered_ID):
            return user

def login():
    entered_id = input("Please enter your Account ID: ")
    current_user = find_user(entered_id)

    if current_user:
        if not current_user.status:
            print("Account is blocked")
            return None

        while current_user.attempts > 0:
            PIN = input(f"Enter PIN for {current_user.name} ({current_user.attempts} attempts left): ")
            if PIN != current_user.PIN:
                current_user.decrease_attempts()
                print("Wrong PIN")
            else:
                print(f"\nWelcome, {current_user.name}!")
                current_user.attempts = 3
                return current_user
    else:
        print("User with this ID not found.")

    return None
        
def logout(user):
    print(f"\nLogging out... See you soon, {user.name}!")
    return False

def close(user):
    print(f"\nThank you for using our ATM, {user.name}!")
    print("Please take your card.")
    exit()

menu = {
    1: ("Check balance", check_balance),
    2: ("Deposit", deposit_money),
    3: ("Withdraw", withdraw_money),
    4: ("Transaction history", account_history),
    5: ("Change PIN", change_PIN),
    6: ("Account info", user_info),
    7: ("Transfer money", transfer_money),
    8: ("Log out", logout),
    9: ("Exit", close)
}

class User:
    def __init__(self, name, balance=0):
        self.ID = random.randint(10000,99999)
        self.name = name
        self.PIN = str(random.randint(0, 9999)).zfill(4)  
        self.balance = balance
        self.history = []    
        self.status = True   
        self.attempts = 3

    def add_to_balance(self, amount):
        self.balance += amount
        self.history.append(f"Deposited: ${amount}")
        print(f"Successfully deposited ${amount}. New balance: ${self.balance}")
    
    def withdraw(self,amount):
        self.balance -= amount
        self.history.append(F"withdrawn: ${amount}")
        print(f"Successfully withdrawn ${amount}. New balance: ${self.balance}")

    def decrease_attempts(self):
        self.attempts -= 1
        if self.attempts <= 0:
            self.status = False
            print("Card blocked!")
        return self.attempts


def start_ATM():
        
    if __name__ == "__main__":
        user1 = User("Dima", 1000)
        user2 = User("Artem", 500)
        users.extend([user1, user2])

        print("--- BANK SYSTEM ONLINE ---")
        print(f"DEBUG: {user1.name} ID: {user1.ID} PIN: {user1.PIN}")
        print(f"DEBUG: {user2.name} ID: {user2.ID} PIN: {user2.PIN}")
        print("-" * 26)

    while True:
        current_user = login()

        if current_user:
            session_active = True
            while session_active:
                print(f"\n--- {current_user.name.upper()}'S MENU ---")
                for key, val in menu.items():
                    print(f"{key}. {val[0]}")
                
                try:
                    choice = int(input("\nChoose option: "))
                    if choice in menu:
                        result = menu[choice][1](current_user)
                        
                        if result is False:
                            session_active = False
                    else:
                        print("Invalid choice, try again.")
                except ValueError:
                    print("Error: Enter only numbers!")

start_ATM()