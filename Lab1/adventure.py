"""
Name: Huiwon Choi
Last updated: 04/09/2026
Description: A simple soccer game.
"""


def adventure():

    print()
    print("Welcome to the Soccer Match!")
    print("Your team is playing in the final.")

    player_name, player_class = create_player()

    print()

    if player_class == "Warrior" or player_class == "warrior":
        health = 100
        mana = 50
        print("You are an attacking player!")
    elif player_class == "Mage" or player_class == "mage":
        health = 70
        mana = 100
        print("You are a creative midfielder!")

    print()
    print("Health: {}".format(health))
    print("Mana: {}".format(mana))

    print()
    print(player_name, "The match is starting!")

    choice = input("Do you want to SHOOT or PASS? [SHOOT / PASS] ")

    if choice == "SHOOT" or choice == "shoot":
        print("You shoot the ball!")
        health -= 20
        print("Your team scores a goal!")

    elif choice == "PASS" or choice == "pass":
        print("You pass the ball to your teammate!")
        mana += 20
        print("Your teammate scores a goal!")

    else:
        print("You missed your chance.")
        health -= 10

    print()
    print("Health: {}".format(health))
    print("Mana: {}".format(mana))

    choice = input("Do you want to ATTACK or DEFEND? [ATTACK / DEFEND] ")

    if choice == "ATTACK" or choice == "attack":
        print("You attack the opponent's goal!")
        health -= 30

    elif choice == "DEFEND" or choice == "defend":
        print("You defend your team's goal!")
        health += 10

    else:
        print("You do nothing.")

    print()
    print("Health: {}".format(health))
    print("Mana: {}".format(mana))

    if health > 50:
        print("Your team wins the match!")
        print("Congratulations,", player_name)
        return 1

    else:
        print("Your team loses the match.")
        print("Better luck next time!")
        return 1


def create_player():
    """Prompts the user for their name and class.
    Arguments: None
    Returns:
        - player_name (string): Name of the player
        - player_class (string): Class of the player
    """

    player_name = input("What is your name? ")
    player_class = input("What is your specialty? [Warrior / Mage] ")

    while player_class != "Warrior" and player_class != "Mage" and player_class != "warrior" and player_class != "mage":
        print("Please choose Warrior or Mage.")
        player_class = input("What is your specialty? [Warrior / Mage] ")

    return player_name, player_class


win = 0

while win == 0:
    win = adventure()