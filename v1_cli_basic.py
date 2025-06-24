import random

def Game(rounds: int = 5):
    choices = ["rock", "paper", "scissor"]
    computer_score = 0
    your_score = 0
  
    print("🎮Welcome to the game")

    for round_num in range(1, rounds + 1):
        print(f"--round{round_num}--")


        you =input(f"Enter your choice: {choices}").lower()
        if you not in choices:
            print("Invalid choice! Please try again.")
            continue
        computer = random.choice(choices)
        print(f"computer choose: {computer}")
        

        if you == computer:
            print("Its a tie")

        elif (you == "rock" and computer == "scissor" or\
             you == "paper" and computer == "rock" or\
             you == "scissor" and computer == "paper"):
            print("You won!")

            your_score += 1
        
        else:
            print("You lose")

            computer_score += 1
        
        print(f"You have Scored {your_score} points:")
        print(f"Computer has Scored {computer_score} points:")
        

    if your_score>computer_score:
        print("You win.....!")
    elif computer_score>your_score:
        print("Shit! You lose....!")
    else:
        print("It's a draw")
Game()

    

