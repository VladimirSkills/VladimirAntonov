import math

class Rectangle:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def get_area(self):
        return self.a * self.b

class Square:
    def __init__(self, a):
        self.a = a
    def get_area_square(self):
        return self.a ** 2

class Circle:
    def __init__(self, r):
        self.r = r
    def get_circle_square(self):
        p = math.pi
        return round(p * self.r ** 2, 2)
    p = math.pi # для вывода числа Pi через класс Circle.p
