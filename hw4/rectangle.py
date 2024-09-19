#chatgpt session link: https://chatgpt.com/c/66ec6eea-9668-8002-aeba-69c15cd457bb

# Defining the Rectangle class with length and width attributes
class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    # Method to calculate the area of the rectangle
    def calculate_area(self):
        return self.length * self.width

# Creating an instance of Rectangle with length = 5 and width = 3
rectangle = Rectangle(5, 3)

# Printing the area of the rectangle
print(f"The area of the rectangle is: {rectangle.calculate_area()}")
