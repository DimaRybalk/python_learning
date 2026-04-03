# Dice Rolling Game
import random, time

def animation(text,x,delay):
    print(text, end="", flush=True) 
    for _ in range(x):      
        time.sleep(delay)     
        print(".", end="", flush=True) 
        time.sleep(0.1)
    print()

def Dice_Rolling():
    answer = input("Would you like to roll a Dice? (y/n) ").lower() 
    counter = 1
    
    while True:
        if answer == "y" and len(answer) < 2:
            animation("Rolling",5,0.25)
            result_1 = random.randint(1,6)
            result_2 = random.randint(1,6)
            print(f"Your result is: {result_1} and {result_2}")
            print(f"Try number: {counter}")
            counter += 1
            answer = input("Would you like to roll a Dice again? (y/n) ").lower()

        elif answer.lower() == "n": 

            animation("Stopping the programm",3,0.25)
            print("Programm stopped")
            break

        else:
            print("You need to type only 'y' or 'n' ")
            answer = input("Would you like to roll a Dice again? (y/n) ").lower()
      
   
Dice_Rolling()

