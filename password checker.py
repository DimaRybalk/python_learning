import string
import time


class PasswordChecker:

    SPECIAL_SYMBOLS = string.punctuation

    def __init__(self,user_password):
        self.password = user_password
        self.score = 0
        self.status = "Very weak"


    def animation(self,text,x,delay):
        print(text, end="", flush=True) 
        for _ in range(x):      
            time.sleep(delay)     
            print(".", end="", flush=True) 
            time.sleep(0.1)
        print()


    def check_all(self):
        self.score = 0
        
        checks = [
        (self._length_check, "Checking length"),
        (self._digit_check, "Searching for digits"),
        (self._uppercase_check, "Verifying case sensitivity"),
        (self._special_checker, "Scanning symbols")
    ]
        
        for method, message in checks:
            self.animation(message, 3, 0.2)
            method() 
            time.sleep(0.3)
        
        if self.score == 4:
            self.status = "Very Strong"
            return True
        elif self.score == 3:
            self.status = "Strong"
            return False
        elif self.score == 2:
            self.status = "Medium"
            return False
        elif self.score == 1:
            self.status = "Weak"
            return False
        else:
            self.status = "Very Weak"
            return False

    def _length_check(self):
        if len(self.password) < 12:
            print("Password too short, you need to type more symbols")
        else:
            self.score += 1 
            print("Length check passed! +1 point")
    
    def _digit_check(self):
        if any(char.isdigit() for char in self.password):
            self.score += 1
            print("Digit check passed! +1 point")
        else:
            print("You need to add at least 1 digit")
            
        
    def _uppercase_check(self):
        if any(char.isupper() for char in self.password):
            self.score += 1
            print("Upper case check passed! +1 point")
        else:
            print("You need to add at least 1 upper case char")
                 
    def _special_checker(self):
        if any(char in self.SPECIAL_SYMBOLS for char in self.password):
            self.score += 1
            print("Special symbol check passed! +1 point")
        else:
            print("You need to add at least 1 special symbol","".join(self.SPECIAL_SYMBOLS))


while True:
    user_password = input("Type your password: ")
    print("\n--- Checking your password ---")
    my_password = PasswordChecker(user_password)
    if my_password.check_all():
        print(f"\nExcellent! Password status: {my_password.status}\n")
        break 
    else:
        print("\nYour password is not safe enough. Try again!\n")