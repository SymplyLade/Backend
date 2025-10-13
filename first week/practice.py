# -create a simple class names Pet,
# -This class should have features name, species and age.
# - Include a function to display the class information.
# -Write a function to celebrate the pet's birthday. 


class Pet:
    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age
    def display(self):
        print(f"Pet Name: {self.name}")
        print(f"Species: {self.species}")
        print(f"Age: {self.age} years old")
    def celebrate_birthday(self):
        self.age += 1
        print(f" Happy Birthday, {self.name}! You are now {self.age} years old!")

animal = Pet("Funfun", "Cat", 2)
animal.display()
animal.celebrate_birthday()
    
   
