ticket = int(input('Укажите кол-во билетов (макс 5 шт): '))
if 0 < ticket <= 5: # ограничение ввода по количеству
    price = 0
    count = 0
    for i in range(ticket):
        while True:
            try:
                count += 1
                age = int(input(f'Возраст {count}-го посетителя: '))
                # Если вводится не число, будет вызвано исключение:
            except ValueError:
                # Цикл будет повторяться до правильного ввода:
                print("Нужно ввести число! Попробуйте снова...")
            else:
                if age < 18:
                    price += 0
                elif 18 <= age < 25:
                    price += 990
                else:
                    price += 1390
                break
    if ticket > 3:
        discount = 0.9
    else:
        discount = 1
    print('Стоимость билетов на', ticket, 'чел:', round(discount * price), 'руб.')

else:
    print('Один может купить не более 5 билетов!')

