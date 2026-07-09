while True:
    password = input("enter your password\n1_it must have least 8 character |\n2_it must have at least one lowercase and one uppercase lettar\n3_it must have least one digit\n4_it must have least one character like these[*, &, ^, %, $, #, @, !]: ")
    

    j = False
    if len(password) < 8:
        j = False
        print("the password is invaild, please try agine.")
        continue

    ju = False
    for i in password:
        if i.isupper():
            ju = True
            break
    if not ju:
        print("the password is invaild, please try agine.")
        continue
    
    jl = False
    for i in password:
        if i.islower():
            jl = True
            break
    if not jl:
        print("the password is invaild, please try agine.")
        continue

    jd = False
    for i in password:
        if i.isdigit():
            jd = True
            break
    if not jd:
        print("the password is invaild, please try agine.")
        continue

    js = False
    sc = ["*", "&", "^", "%", "$", "#", "@", "!"]
    for i in password:
        if i in sc:
            js =True
            break
    if not js:
        print("the password is invaild, please try agine.")
        continue



    
    print("the password is vaild.")
    break