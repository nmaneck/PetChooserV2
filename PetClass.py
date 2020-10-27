# Simple Pet Class. Class variables are publicly accessible.
class Pet:
    def __init__(self, petName, ownerName, petAge, animalType):
        self.petName = str(petName)
        self.ownerName = str(ownerName)
        self.petAge = int(petAge)
        self.animalType = str(animalType)