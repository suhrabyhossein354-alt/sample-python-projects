class atm:
    def __init__(self, balance):
        self.balance = balance


    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print("the deposit was successfully!")

        else:
            print(f"{amount} is not valid, please try again.")


    def withdraw(self, amount):
        if amount > self.balance:
            print(f"{amount} is not valid, please try again.")

        elif amount <= 0:
            print("Invalid amount, please try again.")

        else:
            self.balance -= amount
            print("the withdraw was successfully!")


    def show_balance(self):
        print(f"your balance: {self.balance}")


my_atm = atm(0) 


while True:
    print("-----welcome to ATM-----")
    print("1. show balance\n2. deposit\n3. withdraw\n4. exit")
    print("--------------------------------------------------------------")


    s_atm = input("enter a number between 1 and 4: ")


    if s_atm == '1':
        my_atm.show_balance()
    
    elif s_atm == '2':
        try:
            amount = int(input("enter the desired amount: "))
            my_atm.deposit(amount)

        except ValueError:
            print("Invalid input, please try again.")
    
    elif s_atm == '3':
        try:
            amount = int(input("enter the desired amount: "))
            my_atm.withdraw(amount)
            
        except ValueError:
            print("Invalid input, please try again.")

    elif s_atm == '4':
        print("have a nice day.")
        break

    else:
        print("invalid input, please try again.")