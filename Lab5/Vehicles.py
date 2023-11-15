# Create a base class Vehicle with attributes like make, model, and year, and then 
# create subclasses for specific types of vehicles like Car, Motorcycle, and Truck.
# Add methods to calculate mileage or towing capacity based on the vehicle type.

class Vehicle():
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
    def calculate_mileage():
        pass
    def calculate_towing_capacity():
        pass

class Car(Vehicle):
    def __init__(self, make, model, year, fuel_efficiency, towing_capacity):
        super().__init__(make, model, year)
        self.fuel_efficiency = fuel_efficiency
        self.towing_capacity_value = towing_capacity

    def calculate_mileage(self):
        return f"{self.make} {self.model} ({self.year}) has a mileage of {self.fuel_efficiency} miles per gallon."
    
    def calculate_towing_capacity(self):
        return f"{self.make} {self.model} ({self.year}) has a towing capacity of {self.towing_capacity_value} pounds."
    


class Motorcycle(Vehicle):
    def __init__(self, make, model, year, fuel_efficiency):
        super().__init__(make, model, year)
        self.fuel_efficiency = fuel_efficiency

    def calculate_mileage(self):
        return f"{self.make} {self.model} ({self.year}) has a mileage of {self.fuel_efficiency} miles per gallon."
    
    def calculate_towing_capacity(self):
        return f"This information is not available."



class Truck(Vehicle):
    def __init__(self, make, model, year, fuel_efficiency, towing_capacity):
        super().__init__(make, model, year)
        self.towing_capacity = towing_capacity
        self.fuel_efficiency = fuel_efficiency

    def calculate_mileage(self):
        return f"{self.make} {self.model} ({self.year}) has a mileage of {self.fuel_efficiency} miles per gallon."
    
    def calculate_towing_capacity(self):
        return f"{self.make} {self.model} ({self.year}) has a towing capacity of {self.towing_capacity} pounds."



car = Car("Dacia", "Logan", 2022, 30, 1150)
print(car.calculate_mileage())
print(car.calculate_towing_capacity())

motorcycle = Motorcycle("Harley-Davidson", "Street Glide", 2022, 30)
print(motorcycle.calculate_mileage())
print(motorcycle.calculate_towing_capacity())

truck = Truck("Ford", "F-150", 2022, 30, 10000)
print(motorcycle.calculate_mileage())
print(truck.calculate_towing_capacity())