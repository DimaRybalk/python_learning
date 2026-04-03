import random, time

def animation(text, x, delay):
    print(text, end="", flush=True) 
    for _ in range(x):      
        time.sleep(delay)     
        print(".", end="", flush=True) 
    print()

def start_game():
    while True:
        answer = input("How many times you want to roll the dice? (1-6) ") 
        if answer.isdigit():
            number = int(answer) 
            if 1 <= number <= 6:
                return number 
            else:
                print("Error: You need to type a number from 1 to 6")
        else: 
            print("Error: You need to type a number, not text")

def Dice_Rolling(times):
    for i in range(1, times + 1):
        print("-" * 15)
        animation(f"Roll {i} is rolling", 5, 0.25)
        result_1 = random.randint(1, 6)
        result_2 = random.randint(1, 6)
        print(f"Your result is: {result_1} and {result_2}")
        


while True:
    counts = start_game()
    Dice_Rolling(counts)
    print("-" * 15)
    while True:
        again = input("Would you like to play again? (y/n): ").lower()
        if again == 'y':
            break
        elif again == "n":
              animation("Game is closing", 3, 0.25)
              exit()
        else:
            print("You need to type only y/n")