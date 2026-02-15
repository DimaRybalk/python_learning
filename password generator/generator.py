import random,secrets,string

class PasswordGenerator:

    SPECIAL_SYMBOLS = string.punctuation
    ALPHABET = string.ascii_letters
    DIGITS = string.digits

    def __init__(self,unique = False,alphabet = False,digits = False ,punctuations = False):
        self.unique = unique
        self.alphabet = alphabet
        self.digits = digits
        self.punctuations = punctuations
        
        
    def create_password(self):
        self.password_symbols = ""
        amount = self._create_amount()

        self._set_length()
        self._is_unique()
        self._add_alphabet()
        self._add_digits()
        self._add_punctuations()
        
        passwords_list = []
        

        if not self.password_symbols:
            print("Error: No symbols selected!")
            return None
        
        for i in range(amount):
            if self.unique:
                count = min(self.length, len(self.password_symbols))
                result = random.sample(self.password_symbols, count)
            else:
                result = secrets.choices(self.password_symbols, k=self.length)

            self.final_password = "".join(result)
            current_password = "".join(result)
            passwords_list.append({i+1:current_password})

        while True:
            choice = input("\nDo you want to save these passwords to a file? (y/n): ").lower().strip()
            if choice == 'y':
                self._save_to_file(passwords_list)
                break
            elif choice == "n":
                print("The passwords won't be saved")
                break
            else:
                print("You need to type only 'y' or 'n'")

                

        return passwords_list

    def _add_alphabet(self):
        if self.alphabet:
            self.password_symbols += self.ALPHABET
        else:
            print("You wanted not to add alphabet at your password")

    def _add_digits(self):
        if self.digits:
            self.password_symbols += self.DIGITS
        else:
            print("You wanted not to add digits at your password")

    def _add_punctuations(self):
        if self.punctuations:
            self.password_symbols += self.SPECIAL_SYMBOLS
        else:
            print("You wanted not to add punctuations at your password")

    def _is_unique(self):
        if self.unique:
            return True
        return False
    
    def _create_amount(self):
          while True:
            try:
                self.amount = int(input("Please type the amount of passwords you want to create: "))
                print(f"Amount set to {self.amount}")

                if self.amount > 0:
                    return self.amount
                else:
                    print("Number should be greater than 0")
            except ValueError:
                print("You need to type only numbers")
    
    def _set_length(self):
        while True:
            try:
                self.length = int(input("Please type the length of the password (8-20): "))
                if 8 <= self.length <= 20:
                    print(f"Length set to {self.length}")
                    return self.length
                else:
                    print("Out of range! Please try again.")

            except ValueError:
                print("You need to type only numbers")

    def _save_to_file(self,passwords_list):
        if not passwords_list:
            print("List of passwords is empty")
            return
        
        while True:
            filename = input("Type the name of file you want to create: ").strip()
            if not filename:
                print("You need to type name of file!")
                continue 
            
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    for password in passwords_list:
                        for key, value in password.items():
                            f.write(f"{key} password generated: {value}\n") 
                print(f"You successfully saved {len(passwords_list)} passwords in '{filename}'")
                break
            except Exception as e:
                print(f"Error: {e}")
                break
            
      
            
p1 = PasswordGenerator(unique=True,alphabet=True,punctuations=True,digits=True)
passwords = p1.create_password()


