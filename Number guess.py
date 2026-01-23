import random

def start_game(x,y):
    if not (x.isdigit() and y.isdigit()):
        print("You need to type only numbers")
        return 
    x = int(x)
    y = int(y)
    if x == y:
        print("You need to type different numbers")
    elif x > y:
        print("First number must be lower than second")
    else:
        number = random.randint(x,y)
        print(f"The game has begun, you need to guess the number between {x} and {y}")
        return number

def set_difficulty():
    print("Please choose the difficulty easy(5 attempts)/medium(3 attempts)/hard(1 attempt)")
    
    while True:
        level = input("Please set the difficulty: ").lower()
        if level == "easy":
            print(f"You set {level} difficulty")
            return 5
        elif level == "medium":
            print(f"You set {level} difficulty")
            return 3
        elif level == "hard":
            print(f"You set {level} difficulty")
            return 1
        else:
            print("Invalid input, please type Easy, Medium, or Hard")
          
    
def Answering(answer):
    if not answer.isdigit():
        print("You need to type only numbers")
        return None
    return int(answer)
    
               
while True:
    counter = 0
    first_number = input("Type lower border: ")
    second_number = input("Type higher border: ")
    secret_number = start_game(first_number,second_number)
    print("-" * 15)   
    

    if secret_number is None:
      continue 

    difficulty = set_difficulty()

    while difficulty > 0:
        print("-" * 15)
        answer = input("What is the number?: ")
        player_answer = Answering(answer)

        if player_answer is None:
            continue

        counter += 1
        
        if player_answer == secret_number:
            print(f"You guessed the number in {counter} attempts")
            break
        elif player_answer < secret_number:
            print(f"No, secret number is higher, try again,attempt# {counter}")
            difficulty -= 1
            print(f"{difficulty} attempts left")
            if difficulty == 0:
                print(f"You lost! The secret number was {secret_number}")
        else:
            print(f"No, secret number is lower, try again,attempt# {counter}")
            difficulty -= 1
            print(f"{difficulty} attempts left")
            if difficulty == 0:
                print(f"You lost! The secret number was {secret_number}")
        
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
        
        
        


