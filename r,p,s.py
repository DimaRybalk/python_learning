import random

def start_game(answer):
    choices = ["rock","paper","scissors"]
    if answer not in choices:
        print("You need to type only rock/paper/scissors")
        return False
    else:
        return True

def computer_answer():
   random_choice = random.choice(["rock","paper","scissors"])
   return random_choice

while True:
    player_score = 0
    computer_score = 0
    round_counter = 0

    while (player_score < 3 and computer_score < 3):
        print("-" * 15)
        player_input = input("Rock ,paper or scissors?: ").lower().strip()
        
        
        if not start_game(player_input):
            continue
        
        computer = computer_answer()
        print(f"Your opponent have chosen: {computer}")

        round_counter += 1

        if player_input == computer:
            print(f"Draw 🤝 | round {round_counter} | score {player_score}:{computer_score} ")
        elif (
            (player_input == "rock" and computer == "scissors") or
            (player_input == "scissors" and computer == "paper") or
            (player_input == "paper" and computer == "rock")
        ):
            player_score += 1
            print(f"You win 🎉,| round {round_counter} | score {player_score}:{computer_score}")
        else:
            computer_score += 1
            print(f"You lose 😢| round {round_counter} | score {player_score}:{computer_score}")

    if player_score == 3:
        print("You won the match")
    elif computer_score == 3:
        print("computer won the match")

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
    
