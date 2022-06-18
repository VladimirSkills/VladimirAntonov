"""КОД С ОШИБКОЙ: raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)"""
import json

OPEN_TIME = 10
CLOSE_TIME = 21

def check_date(str_date):
    if len(str_date.split("-")) != 3:  # Получаем количество значений через дефис, если не ровно 3, то ошибка.
        return False
    year, month, day = str_date.split("-")  # 2021 05 26
    if len(year) != 4 or len(month) != 2 or len(day) != 2:
        return False
    # isdigit() возвращает True, если все символы в строке являются цифрами:
    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        return False
    year, month, day = int(year), int(month), int(day)
    if 2000 <= year <= 3000 and 1 <= month <= 12 and 1 <= day <= 31:
        return True
    else:
        return False

def ask_date():
    print("Введите дату: ")
    date = None
    while date is None:
        temp = input()
        if check_date(temp):
            date = temp
        else:
            print("Введена некорректная дата!")
    return date

# Функция, проверяющая число:
def check_int(number, begin, end):
    if not (number.isdigit()):
        return False
    number = int(number)
    return begin <= number <= end

# Функция, запрашивающая число:
def ask_int(begin, end):
    number = None
    while number is None:
        temp = input()
        if check_int(temp, begin, end):
            number = int(temp)
        else:
            print("Введено некорректное число")
    return number

# Сохранение анкеты в файл inform:
def save_into_json(info):
    with open("inform.json", 'w') as write:
        json.dump(info, write)


# Выгрузка анкет из файла:
def load_into_json():
    with open("inform.json") as write:
        info = json.load(write)
    return info


def ask_user():
    print("Введите время ожидания очереди (в часах): ")
    wait = ask_int(0, 12)
    print(f"Введите час, в который вы посещали МФЦ? (от {OPEN_TIME} до {CLOSE_TIME} )")
    hour = ask_int(OPEN_TIME, CLOSE_TIME)
    print("Введите дату посещения (в формате YYY-MM-DD ):")
    date = ask_date()
    return {
        "wait": wait,
        "hour": hour,
        "date": date
    }


def mainhead():
    static = load_into_json()  # Загружаем анкеты, что были
    while True:
        static.append(ask_user())  # Создаём новые анкеты до ответа "нет"
        print("Продолжить заполнение анкет? (да/нет)")
        temp = input()
        if temp.lower() != "да":
            break
    save_into_json(static)

mainhead()