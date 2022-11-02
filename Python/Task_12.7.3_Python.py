"""Вам дан словарь per_cent с распределением процентных ставок по вкладам
в различных банках таким образом, что ключ — название банка, значение — процент.
Напишите программу, в результате которой будет сформирован список deposit значений
— накопленные средства за год вклада в каждом из банков. На вход программы с клавиатуры
вводится сумма money ~ 100 000, которую человек планирует положить под проценты.
Добавьте в программу поиск максимального значения и его вывод на экран."""
from decimal import Decimal

per_cent = {'ТКБ': 5.6, 'СКБ': 3.9, 'ВТБ': 4.28, 'СБЕР': 4.05}
money = int(input("Введите сумму вклада в рублях: "))
b1 = per_cent.get('ТКБ')
b2 = per_cent.get('СКБ')
b3 = per_cent.get('ВТБ')
b4 = per_cent.get('СБЕР')
bank1 = round(b1 / 100 * money)
bank2 = round(b2 / 100 * money)
bank3 = round(b3 / 100 * money)
bank4 = round(b4 / 100 * money)

deposit = [bank1, bank2, bank3, bank4]
print("Money =", money, "руб.")
print("Bank =", (', '.join(per_cent.keys())))
print("Deposit =", deposit)
print("Максимальная сумма, которую вы можете заработать —", max(deposit), "руб.")

print("\nИЛИ ЭДАК:")


def numformat(num):
    n = Decimal(str(num))
    number = n.quantize(Decimal("1.00"))
    formi = '{0:,}'.format(number).replace(',', ' ')
    return formi


for i in per_cent:
    p = per_cent[i] / 100 * money
    for j in per_cent:
        if j == i:
            print(f'Доход {numformat(p)} по ставке {round(per_cent.get(i), 2)}% в банке: {j}')
maxi = max(per_cent.values()) / 100 * money
bank = max(per_cent, key=per_cent.get)
symbol = u'\u2605'
print(f"|{symbol*3}|Лучшее предложение: в банке {bank} с доходом: {numformat(maxi)} руб.")
