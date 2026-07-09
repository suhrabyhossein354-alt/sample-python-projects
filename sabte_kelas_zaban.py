def first_name():
    while True:
        fn = input("enter your first name: ")
        if not fn.strip():
            print("your name is invaild, please try agine.")
        else:
            return fn
            
def last_name():      
    while True:
        ln = input("enter your last name: ")
        if not ln.strip():
            print("your name is invaild, please try agine.")
        else:
            return ln

def age():
    while True:
        age = input("enter your age: ")
        if not age.isdigit():
            print("your age is invaild, please try agine.")
        else:
            age = int(age)
            if age < 0:
                 print("your age is invaild, please try agine.")
            else:
                return age

def shomare():
    while True:
        sh = input("enter your number: ")
        if not sh.isdigit():
            print("your number invaild, please try agine.")
        else:
            if len(sh) != 11:
                print("your number invaild, please try agine.")
            else:
                return int(sh)
            
def email():
    while True:
        em = input("enter your email addres[it must have example@gmail.com]: ")
        if "@gmail.com" in em:
            return em
        else:
            print("your email is invaild, please try agine.")

def sz():
    while True:
        sz = input("enter your language level\nbeginner or middle or professional: ")
        if "beginner" in sz:
            return sz
        elif "middle" in sz:
            return sz
        elif "professional" in sz:
            return sz
        else:
            print("your input is invaild, please try agine.")



a1 = first_name()
a2 = last_name()
a3 = age()
a4 = shomare()
a5 = email()
a6 = sz()



#-------------------------------------------------------------------------------------------



print("-----your info-----")
print(f"name: {a1} {a2}")
print(f"age: {a3}")
print(f"number: {a4}")
print(f"email: {a5}")
print(f"level: {a6}")