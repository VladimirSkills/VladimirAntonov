while True:
    try:
        a = list(map(int, input('Укажите произвольный набор чисел через запятую: ').split(',')))
        # Если ошибка, будет вызвано исключение:
    except Exception:
        # Цикл будет повторяться до правильного ввода:
        print("<<Ошибка!>> Пример ввода чисел: 22,5,85,14,6,40")
    else:
        break

while True:
    try:
        b = list(map(int, input(f'Введите число от {min(list(a))} до {max(list(a))}: ').split(',')))
        if min(list(b)) < min(list(a)) or min(list(b)) > max(list(a)):
            raise ValueError
        # Если ошибка, будет вызвано исключение:
    except ValueError:
        # Цикл будет повторяться до правильного ввода:
        print(f"Нужно ввести число от {min(list(a))} до {max(list(a))}!")
    else:
        break

# Преобразование введённой последовательности в список:
array, num = list(map(int, a)), list(map(int, b))
array.extend(num) # вставляем значение в конец списка
print("Список чисел:", array)

# Сортировка:
def sortArray(array):
    for i in range(1, len(array)):
        x = array[i]
        p = i
        while p > 0 and array[p - 1] > x:
            array[p] = array[p - 1]
            p -= 1
        array[p] = x
    return array
sortA = sortArray(array)
print("Сортировка:", sortA)


# Поиск индекса числа, предшествующего введённому:
def double_search(sortA, element, left, right):
    if left > right:  # если левая граница превысила правую,
        return False  # значит элемент отсутствует

    middle = (right + left) // 2  # находим середину
    if element == sortA[middle]:  # если элемент в середине,
        return middle  # возвращаем этот индекс
    elif element < sortA[middle]:  # если элемент меньше элемента в середине
        # рекурсивно ищем в левой половине
        return double_search(sortA, element, left, middle - 1)
    else:  # иначе в правой
        return double_search(sortA, element, middle + 1, right)

element = min(b) # переводим в формат числа
idx = double_search(sortA, element, 0, len(sortA))

# Обработка исключения при вводе значения = мин или макс в списке:
if element == max(sortA):
    Pidx = idx
elif element == min(sortA):
    Pidx = "- не определён, так как введённое число минимальное"
else:
    Pidx = idx - 1

print(f"Последний индекс в списке: {len(sortA)-1}")
print(f"Предшествующий числу {element} индекс:", Pidx)

# Укажите произвольный набор чисел через запятую: 25,45,6,8,54,10,65,88,70,3,56,4,80,95,2
# Введите число от 2 до 95: 84
# Список чисел: [25, 45, 6, 8, 54, 10, 65, 88, 70, 3, 56, 4, 80, 95, 2, 84]
# Сортировка: [2, 3, 4, 6, 8, 10, 25, 45, 54, 56, 65, 70, 80, 84, 88, 95]
# Последний индекс в списке: 15
# Предшествующий числу 84 индекс: 12