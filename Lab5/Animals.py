# Create a class hierarchy for animals, starting with a base class Animal. Then, create 
# subclasses like Mammal, Bird, and Fish. Add properties and methods to represent characteristics 
# unique to each animal group.


class Animal:
    def __init__(self, name, habitat):
        self.name = name
        self.habitat = habitat

    def move(self, ways):
        print(f"This animal named {self.name} can move by {ways}")

    def print_habitat(self):
        print(f"This animal named {self.name} lives in {self.habitat}")

class Mammal(Animal):
    def __init__(self, name, habitat, fur_color):
        super().__init__(name, habitat)
        self.fur_color = fur_color

    def produce_milk(self):
        print(f"{self.name} is producing milk to nourish its young.")


class Bird(Animal):
    def __init__(self, name, habitat, wingspan):
        super().__init__(name, habitat)
        self.wingspan = wingspan

    def print_wingspan(self):
        print(f"{self.name} has a wingspan of {self.wingspan}.")

class Fish(Animal):
    def __init__(self, name, habitat, fin_type):
        super().__init__(name, habitat)
        self.fin_type = fin_type

    def print_fin_type(self):
        print(f"{self.name} is swimming and its fin-type is {self.fin_type}.")

lion = Mammal("Lion", "Grasslands", "Golden")
lion.produce_milk()  
lion.move("walking")
lion.print_habitat()

sparrow = Bird("Sparrow", "Forests", 20)
sparrow.print_wingspan()

shark = Fish("Shark", "Oceans", "Dorsal")
shark.print_fin_type()




