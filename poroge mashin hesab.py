while True:
    my = u1 = float(input("enter number:"))  

    u2 = input("choise(+ _|_ - _|_ * _|_ / _|_ ** _|_ //) or =:")

    u3 = float(input("enter number:"))

    if u2 == "+" and "-" and "*" and "/" and "**" and "//":
        g = True
    else:
        g = False
        print("invalid input")
        
    if u2 == "+":
        a = u1 + u3
    elif u2 == "-":
        a = u1 - u3
    elif u2 == "*":
        a = u1 * u3
    elif u2 == "/":
        a = u1 / u3
    elif u2 == "**":
        a = u1 ** u3
    elif u2 == "//":
        a = u1 // u3

    print(f"{u1} {u2} {u3} = {a}")


    ah = input("baraye khoroj benevis:k\ndar gheir in sorat benevise:a\n.......")

    if ah == "a":
        continue
    elif ah == "k":
        break
    else:
        print("eshtebah")
        break