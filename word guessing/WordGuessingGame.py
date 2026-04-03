import json,random,string

ALPHABET = string.ascii_letters
score = { 
        "win": 0,
        "lost": 0,
        }

difficulty = {
    1 : "easy",
    2 : "medium",
    3 : "hard"
}


def get_data():
    with open("word.json","r",encoding="utf-8") as file:
        return json.load(file)
    

data = get_data()


def choose_random_word(data):
    return list(random.choice(data)) 


def painting_symbols(word,guessed_letters):
    for char in word:
        if char in guessed_letters:
            print(char, end="")
        else:
            print("_", end="")
    print()


def paint_hidden_word(word):
    for _ in range(len(word)):
        print("_", end="")
    print()


def guessing_letters(guessed_letters,word):
    while True:
        letter = input("Enter a letter: ").lower().strip()
       
        if letter not in ALPHABET or len(letter) != 1:

            if letter == "hint":
                remaining = [char for char in word if char not in guessed_letters]
                if remaining:
                    hint_letter = random.choice(remaining)
                    guessed_letters.append(hint_letter)
                    print(f"You used a hint, a letter is {hint_letter}")
                    return True
            else:
                print("You need to choose only from: ","".join(string.ascii_letters))

            return False

        if letter in word:
            if letter not in guessed_letters:
                guessed_letters.append(letter)
                print("Good guess!")
                return True
            else:
                print("You already guessed this.")
                return True
        else:
            print("There are no such letter")
            return False
        

def set_difficulty(prompt):
    diffilties = [diff for diff in difficulty]
    while True:
        try:
            player_answer = int(input(prompt))
            if player_answer not in diffilties:
                print("Invalid choice! Choose 1, 2, or 3.")
                continue 

            if player_answer == 1:
                return 9
            elif player_answer == 2:
                return 6
            else:
                return 3
        except ValueError:
            print("You need to type only number")

def play_game():
    word = choose_random_word(data)
    tries = set_difficulty("Please choose the difficulty number (1 - easy /2 - medium /3 - hard)")
    guessed_letters = []
    paint_hidden_word(word)

    while tries > 0:

        if not guessing_letters(guessed_letters, word):
            tries -= 1
            print(f"Tries left {tries}")

        painting_symbols(word,guessed_letters)

        if all(char in guessed_letters for char in word):
            print("Congratulations! You won!")
            score["win"] += 1
            print(f"The score now is {score["win"]} : {score['lost']} ")
            break

        if tries == 0:
            print("You lost, the word was:","".join(word))
            score["lost"] += 1
            print(f"The score now is {score["win"]} : {score['lost']}")
            break


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
