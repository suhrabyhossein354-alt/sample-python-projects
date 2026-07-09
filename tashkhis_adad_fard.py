while True:
    number = input("enter a 5 digit number: ")


    if not number.isdigit() or len(number) != 5:
        print("the number is wrong, please try agine")
        continue
    else:
        odd_numbers = 0
    break

for digit in number:
    if int(digit) % 2 != 0:
       odd_numbers += 1



if odd_numbers == 0:
    print("there are no odd number!")

else:
    print(f"number of odd digits: {odd_numbers}")