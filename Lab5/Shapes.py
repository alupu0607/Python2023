# Create a class hierarchy for shapes, starting with a base class Shape. 
# Then, create subclasses like Circle, Rectangle, and Triangle. 
# Implement methods to calculate area and perimeter for each shape.

import math

class Shape:
    def area(self):
        pass

    def perimeter(self):
        pass

    def print_details(self):
        print(f"Area: {self.area()}, Perimeter: {self.perimeter()}")

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius

    def print_details(self):
        print(f"Circle - Radius: {self.radius}")
        super().print_details()



class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)

    def print_details(self):
        print(f"Rectangle - Length: {self.length}, Width: {self.width}")
        super().print_details()

class Triangle(Shape):
    def __init__(self, side1, side2, side3):
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3

    def area(self):
        s = (self.side1 + self.side2 + self.side3) / 2
        return math.sqrt(s * (s - self.side1) * (s - self.side2) * (s - self.side3))

    def perimeter(self):
        return self.side1 + self.side2 + self.side3
    
    def print_details(self):
        print(f"Triangle - L1: {self.side1}, L2: {self.side2}, L3: {self.side3}")
        super().print_details()

shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]

for shape in shapes:
    shape.print_details()
    shape.perimeter()
    shape.area()


