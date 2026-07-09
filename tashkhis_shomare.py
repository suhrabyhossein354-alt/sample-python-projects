while True:
    u_number = input("enter your number: ")

    t_unumber = u_number.replace("+", "")
    
    j = False

    if not t_unumber.isdigit():
        j = False
    
    elif u_number.startswith("09") and len(t_unumber) == 11:
        j = True

    elif u_number.startswith("+989") and len(t_unumber) == 12:
        j = True
    
    else:
        j = False

    if j == False:
        print("your number has problem, please try again.")
        continue
    else:
        print("your number is valid.")
        break
