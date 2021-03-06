"""Online wallet / 16.9"""

clients = {
    "client1": {
            'name': 'ivan',
            'surname': 'petrov',
            'city': 'Kirov',
            'balance': 500
        },
    "client2": {
            'name': 'sergey',
            'surname': 'smirnov',
            'city': 'Perm',
            'balance': 4050
        },
    "client3": {
            'name': 'anna',
            'surname': 'ivanova',
            'city': 'Vladivostok',
            'balance': 300
        }
}

class Clients:
    def __init__(self, name, surname, city, balance):
        self.name = name
        self.surname = surname
        self.city = city
        self.balance = balance
    def __str__(self):
        return f'{self.name} {self.surname}, г.{self.city}, баланс: {self.balance} руб.'

    def guests(self):
        return f'{self.name} {self.surname}, город: {self.city}'

one = clients["client1"].values()
print(Clients(*one))

# for key, val in clients.items():
#     allval = list(val.values())
#     # print(f'{key}:')
#     print(Clients(*allval))

print("\nGuests:")
for key, val in clients.items():
    allval = list(val.values())
    out = Clients(*allval)
    print(Clients.guests(out))


# for key, val in clients.items():
#     allval = list(val.values())
#     print(key, *allval)  # выводим клиентов и все значения по нему


# for key, val in clients.items():
#     print(key, val['name'])  # выводим клиентов и значения по ключу


# for key, val in clients.items():
#     print(val['name'])  # выводим все значения по ключу


# get1 = clients.get("client1")
# for val in get1.values():
#     print(val)  # получаем значения


# get1 = clients.get("client1")
# for val in get1:
#     print(val) # поучаем ключи


# list1 = clients["client1"]['name']  # clients["client1"][0]["3-ий уров. вложенности"]['name']
# print(list1)  # ivan


# for x in clients["client1"].values():
#     print(x)  # Все значения по клиенту


# for i in clients:
#     print(i)  # Список клиентов
