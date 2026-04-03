import random

SYMBOLS = ["🍒", "🔔", "💎"]


def starting_balance(prompt):
    while True:
        try:
            balance = int(input(prompt))
            if balance > 49:
                return balance
            else:
                print("balance need to be greater than 49")
                continue
        except ValueError:
            print("You need to type only numbers!")


def bet_amount(prompt,balance):
    while True:
        try:
            bet = int(input(prompt))
            if 0 < bet <= balance:
                return bet
            elif bet < 0:
                print(f"Bet must be greater than 0 and no more than {balance}")
            else:
                print(f"bet can't be greater than {balance}")
                continue
        except ValueError:
            print("You need to type only numbers!")

def calculate_current_balance(win_result, balance, bet):
    if win_result == 1:
        print(f"Jackpot! You won ${bet * 10}")
        return balance - bet + (bet * 10)
    elif win_result == 2: 
        print(f"Small win! You won ${bet * 2}")
        return balance - bet + (bet * 2)
    else:
        print("No luck this time.")
        return balance - bet

def spin_slot():
    return random.choices(SYMBOLS, k=3)

def check_win(spin_result):
    if len(set(spin_result)) == 3:
        return 3
    elif len(set(spin_result)) == 2:
        return 2
    elif len(set(spin_result)) == 1:
        return 1
    
def spin_again(balance):
     while True:
        again = input("Spin again? (y/n): ").lower()
        if again == 'n':
            print(f"Thanks for playing, you won {balance}")
            return False
        elif again == "y":
            break 
        else:
            print("You need to type only y/n")
        
def play_game():
    balance = starting_balance("Enter your starting balance (balance need to be greater than 49): ")
    print("Welcome to the Slot Machine Game!")
    print(f"You start with a balance ${balance}")

    while balance > 0:

        print("-" * 15)
        bet = bet_amount("Enter your bet amount: ",balance)
        spin_result = spin_slot()
        print(" | ".join(spin_result))
        win_result = check_win(spin_result)
        balance = calculate_current_balance(win_result,balance,bet)
        print(f"Your current balance is ${balance}")
    
        if balance > 0:
            if spin_again(balance) == False: 
                break
            
    if balance <= 0:
        print("You lost, better luck next time")

def play_again():
    while True:
        print("-" * 15)
        again = input("Play again? (y/n): ").lower()
        print("-" * 15)
        if again == 'n':
            print("Thanks for playing")
            print("-" * 15)
            exit()
        elif again == "y":
            break 
        else:
            print("You need to type only y/n")

while True:
    play_game()
    play_again()
            


