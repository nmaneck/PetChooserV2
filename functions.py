from PetClass import Pet

# Defines valid strings to quit. Input will be lower cased and checked against this list
quitCommands = {"q", "quit"}

# A function that prints a friendly message before exiting the program.
def quitter():
    print("Thanks for using the pet database! Bye!")
    exit()

# A function for waiting for user input before proceeding, with error catchers built in if the user tries something
# odd
def waiter():
    try:
        input("Press [ENTER] to continue.")
    # Error messages in case the user tries something odd with the waiting message
    except EOFError:
        print("Detected quit command from user, exiting...")
        quitter()
    except Exception as e:
        print(f"Unhandled exception: {e}. Quitting for safety.")
        quitter()

# Command to load list of pets from sql into a python list
def loadPets(connection):
    #SQL Command to retrieve the desired data
    petConnector = """
        select 
            pets.id,
            pets.name as petName,
            pets.age,
            owners.name as ownerName, 
            types.animal_type as animalType
        from pets 
            join owners on pets.owner_id = owners.id 
            join types on pets.animal_type_id = types.id;
        """

    # Executes SQL command defined at beginning then moves all information into a dictionary.
    with connection.cursor() as cursor:
        cursor.execute(petConnector)
        petDict = cursor.fetchall()

    # Takes dictionary and turns it into a list of Pet objects, then function returns list
    listOfPets = list()
    for pet in petDict:
        listOfPets.append(Pet(pet["petName"],
                              pet["ownerName"],
                              pet["age"],
                              pet["animalType"]))
    return listOfPets

# An editor function to change the name and/or age of a pet. Note editor function is only called by
# quitContinueEdit()
def editor(petID, connection, listOfPets):
    # Creates an index variable that starts at 0 for reading the list of pets
    listIndex = petID - 1
    print(f"You have chosen to edit " + listOfPets[listIndex].petName)

    # Attempts to get user input for name and age. Note checks for quit commands and errors, and that age
    # is between 0 and 200 (I dunno, maybe someone has a really old sea turtle)
    try:
        newName = input("New name: [ENTER == no change] \n")
        if newName in quitCommands:
            quitter()
        elif newName == "":
            newName = listOfPets[listIndex].petName
            print("Pet's name will remain unchanged: " + newName)
        else:
            print("Name will be updated. \nOld name: " + listOfPets[listIndex].petName + "\nNew name: " + newName)
        newAge = input("New age: [ENTER == no change] \n")
        if newAge in quitCommands:
            quitter()
        elif int(newAge) not in range(0, 201):
            print("Illegal value for pet age: Must be integer between 0 and 200.")
            newAge = str(listOfPets[listIndex].petAge)
            print("Pet age will remain unchanged: " + newAge)
        elif newAge == "":
            newAge = str(listOfPets[listIndex].petAge)
            print("Pet age will remain unchanged: " + newAge)
        else:
            print("Age will be updated to " + newAge)
    except EOFError:
        print("Detected quit command from user, exiting...")
        quitter()
    except Exception as e:
        print(f"An error has occurred: {e}")
        print("Exiting...")
        print()
        exit()

    # Creates edit command and sends it through sql connection. Note since output is not required, no fetch is
    # performed.
    editCommand = "update pets set age = " + newAge + ", name = \"" + newName + "\" where id = " + str(petID) + ";"
    with connection.cursor() as cursor:
        cursor.execute(editCommand)
    print("Updates saved!")
    waiter()

# Asks user if they would like to quit, continue, or edit. If input is not one of these three options, repeats
# the question via recursion
def continueQuitEdit(petChoice, connection, listOfPets):
    try:
        command = input("Would you like to [C]ontinue, [Q]uit, or [E]dit this pet?")
        editCommands = {"e", "edit"}
        continueCommands = {"c", "continue"}
    except EOFError:
        print("Detected quit command from user, exiting...")
        quitter()
    except Exception as e:
        print(f"An error has occurred: {e}")
        print("Exiting...")
        print()
        exit()
    else:
        if command in quitCommands:
            quitter()
        elif command in editCommands:
            editor(petChoice, connection, listOfPets)
        elif command in continueCommands:
            pass
        else:
            print("Invalid choice. Try again.")
            continueQuitEdit(petChoice, connection, listOfPets)
