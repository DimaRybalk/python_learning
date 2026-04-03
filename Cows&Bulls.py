import random

difficulties = {
    "easy": 10,
    "medium": 8,
    "hard": 5,
}

def set_length(prompt):
   while True:
        try:
            length = int(input(prompt))
            if 4 <= length <= 10:   
                return length
            else:
                 print("You need to choose between 4 and 10")
        except ValueError:
                print("You should type only numbers")

def set_difficulty():
    while True:
        difficulty = input("Choose the difficulty (easy/medium/hard): ").lower()
        if difficulty in difficulties.keys():
            return difficulties[difficulty]
        else:
            print("You need to type only easy/medium/hard")

def create_number(word_length):
     return random.sample("0123456789", word_length)

def player_answer(created_number):
    expected_len = len(created_number)
    while True:
        user_input = input(f"Guess ({expected_len} digits): ")
        answer = list(user_input)
        
        if len(answer) != expected_len:
            print(f"Error: You need to type exactly {expected_len} digits.")
            continue
        
        if not user_input.isdigit():
            print("Error: Please enter only numbers (0-9).")
            continue
            
        if len(set(answer)) != expected_len:
            print("Error: All digits must be unique.")
            continue
            
        return answer
    
def bulls_and_cows_counter(created_number, answer):
    bulls = 0
    cows = 0
    for index,digit in enumerate(answer):
        if digit == created_number[index]:
            bulls += 1
        elif digit in created_number:
            cows += 1
    return bulls,cows

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

def play_game():
    tries = 1
    word_length = set_length("Type word length (4-10): ")
    game_difficulty = set_difficulty()
    created_number = create_number(word_length)
    print(created_number)
    print(f"I have generated a {word_length}-digit number with unique digits. Try to guess it!")

    while tries <= game_difficulty:

        answer = player_answer(created_number)

        if answer == created_number:
           print(f"Congrats, you won!!! in {tries} tries")
           return
        
        bulls,cows = bulls_and_cows_counter(created_number,answer)
        print(f"{bulls} bulls, {cows} cows, try number {tries} of {game_difficulty}")
        tries += 1

    print(f"The number was {''.join(created_number)}, you lost")


while True:
    play_game()
    play_again()



