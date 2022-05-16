"""Rectangle area"""

print('<<< Rectangle area >>>')
class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def getArea1(self):
        return self.x * self.y
    def getArea2(self):
        return self.width * self.height

    def __str__(self):
        #return self.x, self.y, self.width, self.height
        return f'{self.x}, {self.y}, {self.width}, {self.height}'

xy = Rectangle(5, 10, 50, 100)

#print(xy.x)
print(f"Rectangle: {xy.__str__()}")
print(f"Square1: {xy.getArea1()}")
print(f"Square2: {xy.getArea2()}")



"""Online wallet"""

print('\n<<< Online wallet >>>')
class Clients:
    def __init__(self, name, surname, city, balance):
        self.name = name
        self.surname = surname
        self.city = city
        self.balance = balance
    def __str__(self):
        return f'{self.name} {self.surname}, г.{self.city}, Баланс: {self.balance} руб.'

    def guests(self):
        return f'{self.name} {self.surname}, г.{self.city}'

client1 = Clients('Иван', 'Петров', 'Москва', 50)
client2 = Clients('Радомир', 'Светлов', 'Аркаим', 120)
client3 = Clients('Влад', 'Васнецов', 'Самара', 87)
print(f"client 1: {client1}")

guests_list = [client1, client2, client3]
for guest in guests_list:
    print(guest.guests())











