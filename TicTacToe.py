sizes = ["small","medium","large"]
x_wins = 0
o_wins = 0

def size_validator():
    while True:
        size = input("Which size do you want to play (small/medium/large): ").lower()
        if size not in sizes:
            print("you need to only type available options:", ", ".join(sizes))
        else:
            if size == "small":
                return 3
            elif size == "medium":
                return 4
            elif size == "large":
                return 5

def field_draw(field):
    for row in field:
        print("  ".join(row))

def player_turn(current_player):
    print("-"*15)
    print(f"Player {current_player}'s turn")
    
def switch_player(current_player):
    return "O" if current_player == "X" else "X"
      
def turn_validator(prompt,field_size):
    while True:
        try:
            turn = int(input(prompt))
            if 0 <= turn < field_size:
                return turn
            print(f"You should type number between 0 and {field_size-1}")
        except ValueError:
            print("You should type only numbers")

def is_cell_free(field, row, col):
    return field[row][col] == "."

def check_win(field, current_player):
    for row in range(len(field)):
        if all(cell == current_player for cell in field[row]):
            return True

    for col in range(len(field)):
        if all(field[r][col] == current_player for r in range(len(field))):
            return True

    if all(field[i][i] == current_player for i in range(len(field))):
        return True

    if all(field[i][len(field)-1-i] == current_player for i in range(len(field))):
        return True

    return False

def check_draw(field):
    return all(cell != "." for row in field for cell in row)

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
    field_size = int(size_validator())
    field = [["." for _ in range(field_size)] for _ in range(field_size)]
    current_player = "X"
    global x_wins,o_wins

    while True:

        player_turn(current_player)


        row = turn_validator(f"Enter row (0 - {field_size-1}): ", field_size)
        col = turn_validator(f"Enter col (0 - {field_size-1}): ", field_size)


        if is_cell_free(field, row, col):
            field[row][col] = current_player
            field_draw(field)


            if check_win(field, current_player):
                print(f"Player {current_player} wins!")
                if current_player == "X":
                    x_wins += 1
                else:
                    o_wins += 1               
                break
 
            if check_draw(field):
                print("Draw!")
                print(f"Score: X = {x_wins}, O = {o_wins}")
                break
            
            current_player = switch_player(current_player)
        else:
            print("Cell is already occupied! Try again.")

while True:
    play_game()
    play_again()
   

    
