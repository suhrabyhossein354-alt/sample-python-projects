import random

options = ["rock", "paper", "scissors"]

game_rounds = 0
user_score = 0
computer_score = 0

print("game started")

while game_rounds < 6:

    while True:
        user_choice = input("choice(rock, paper, scissors): ").lower()
        if user_choice in options:
            break
        print("your input is invaild, please try agine.")


    computer_choice = random.choice(options)
    print(f"computer choice: {computer_choice}")


    if user_choice == computer_choice:
        print("draw")
        game_rounds += 1
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissors" and computer_choice == "paper"):
        print("you win the round")
        user_score += 1
        game_rounds += 1
    else:
        print("computer win the round")
        computer_score += 1
        game_rounds += 1


    print(f"round: {game_rounds} | your score: {user_score} | computer score: {computer_score}")

if game_rounds == 6:
    if user_score > computer_score:
        print("you win the game!")
    elif user_score < computer_score:
        print("computer win the game!")
    else:
        print("game is draw")
  
