from Square_1 import Rectangle, Square, Circle

# Создадим два прямоугольника
rect_1 = Rectangle(3, 4)
rect_2 = Rectangle(12, 5)
# Выводим площадь прямоугольников
# print(rect_1.get_area())
# print(rect_2.get_area())

square_1 = Square(5)
square_2 = Square(10)
# print(square_1.get_area_square(), square_2.get_area_square())
circle_1 = Circle(7)

figures = [rect_1, rect_2, square_1, square_2, circle_1]

for figure in figures:
    if isinstance(figure, Square):
        print(figure.get_area_square())
    elif isinstance(figure, Circle):
        print(f'Площадь круга (Pi x r^2) = {figure.get_circle_square()}, где Pi = {round(Circle.p, 3)}')
    else:
        print(figure.get_area())



