import random

def switch_player(current_player):
    return "Player 2" if current_player == "Player 1" else "Player 1"

def show_player(current_player):
    print(f"{current_player} turn")

def throw_dice():
   return random.randint(1,6)
    
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


def set_goal(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
                print("You should type only numbers")

def play_game():
    current_player = "Player 1"
    turn_number = 0 
    scores = {"Player 1": 0, "Player 2": 0}
    
    goal = set_goal("How many points you want to reach?: ")
    
    while max(scores.values()) < goal:
        turn_number += 1
        turn_score = 0 
        print(f"\n" + "="*20)
        print(f"TURN {turn_number}")
        
        while True:
            print("-" * 15)
            show_player(current_player)
            roll = throw_dice()
            print(f"You rolled: {roll}")

            if roll == 1:
                print("Ouch! Rolled 1. Turn lost.")
                current_player = switch_player(current_player)
                print(f"Current Score -> P1: {scores['Player 1']}, P2: {scores['Player 2']}")
                break 

            turn_score += roll
            print(f"Turn score: {turn_score} (Total potential: {scores[current_player] + turn_score})")

            if scores[current_player] + turn_score >= goal:
                scores[current_player] += turn_score 
                print(f"!!! {current_player} wins with {scores[current_player]} points! !!!")
                return 

            while True:
                choice = input("Roll again (y/n)?: ").lower()
                if choice in ['y', 'n']:
                    break
                print("Invalid input! Please type 'y' or 'n'.")

            if choice == 'n':
                scores[current_player] += turn_score 
                print(f"Action: {current_player} HOLDS.")
                print(f"Score -> P1: {scores['Player 1']}, P2: {scores['Player 2']}")
                current_player = switch_player(current_player)
                break
    
while True:
    play_game()
    play_again()