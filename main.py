import pymysql
from getpass import getpass
from functions import (waiter, quitter, loadPets, continueQuitEdit)

# Defines valid strings to quit. Input will be lower cased and checked against this list
quitCommands = {"q", "quit"}

# Asks for mysql password and creates connection to mySQL. Allows for quitting, both by QUIT command or ctrl-D
try:
    password = getpass("Input mysql password (or type QUIT):")
    if password.lower() in quitCommands:
        quitter()
    myConnection = pymysql.connect(host="localhost",
                                   user="root",
                                   password=password,
                                   db="pets",
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)
except EOFError:
    print("Detected quit command from user, exiting...")
    quitter()
except Exception as e:
    print(f"An error has occurred: {e}")
    print("Exiting...")
    print()
    exit()


# Loop to display options. Note that loop will continue until program is exited
while True:
    # Refreshes list of pets from SQL
    listOfPets = loadPets(myConnection)
    # Prints list, with one line for each pet.
    print("Choose a pet from the list below:")
    for i in range(0, len(listOfPets)):
        print("[", i+1, "]", listOfPets[i].petName)
    print("[ Q ] Quit")

    # After printing list, asks for input.
    try:
        choice = input()
        # Check if quit command is inputted
        if choice.lower() in quitCommands:
            quitter()
        # Attempts to turn input into integer
        choice = int(choice)
        if choice not in range(1, len(listOfPets) + 1):
            raise ValueError
    # Returns error message and waits if input is not an integer in the range.
    # Note we return to beginning of while loop after this message.
    except ValueError:
        print("Invalid selection. Please choose a number on the list.")
        print()
        waiter()
    # Allows quitting with Ctrl-D
    except EOFError:
        print("Detected quit command from user, exiting...")
        quitter()
    # Exits for unhandled exceptions
    except Exception as e:
        print(f"Unhandled exception: {e}. Quitting for safety.")
        quitter()
    # If valid input is detected, print pet information. Note loop restarts afterwards
    else:
        print("You have chosen " + listOfPets[choice - 1].petName + " the " + listOfPets[choice - 1].animalType + ".",
              listOfPets[choice - 1].petName + " is " + str(listOfPets[choice - 1].petAge) + " years old.",
              listOfPets[choice - 1].petName + "'s owner is " + listOfPets[choice - 1].ownerName + ".")
        print()
        continueQuitEdit(choice, myConnection, listOfPets)