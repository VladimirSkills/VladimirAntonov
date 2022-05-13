"""
Программа, которая получает от пользователя имя файла,
открывает этот файл в текущем каталоге, читает его и выводит два слова,
наиболее часто встречающееся из тех, что имеют размер более трёх символов,
и наиболее длинное слово на английском языке.
"""
import operator
import re

filename = input('Укажите имя файла: ')
ftype = input('Укажите тип файла (расширение): ')
xfile = filename + '.' + ftype # <class 'str'> тип txt имя Testfile, из текущего каталога

# Функция для поиска самого длинного англ. слова:
def longWord(text):
    r = re.compile("([a-zA-Z]+)") # применяем регулярные выражения
    long_word = []
    for english in filter(r.match, text):
        long_word.append(english)
    return long_word

# открываем файл, читаем, приводим текст к нижнему регистру,
# убираем знаки пунктуации, получаем список слов (цифры не учитываем)
with open(xfile, encoding="utf8") as f:
    lst = f.read().lower().translate(
        str.maketrans('', '', '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~—')
    ).split()
# составляем словарь подсчёта
y = 3 # выводим слова длиною > y
res = {x:lst.count(x) for x in lst if len(x) > y} # по кол-ву символов в слове
# Модуль operator включает в себя функцию itemgetter(). Она возвращает значение словаря с ключом, который = 1:
# всё это сортируем по возрастанию....
sorted_res = dict(sorted(res.items(), key=operator.itemgetter(1)))
print(f'Слова, длинною более {y}-х символов:')
print(f'1-ое слово: "{max(sorted_res, key=(sorted_res.get))}" - {max(sorted_res.values())} шт') # первое из наиболее часто встречающихся

sorted_res.pop(max(sorted_res, key=(sorted_res.get))) # Исключаем первый максимум...
print(f'2-ое слово: "{max(sorted_res, key=(sorted_res.get))}" - {max(sorted_res.values())} шт')

print(f'Самое длинное англ. слово: "{max(longWord(lst), key=len)}"')
print(f'Самое длинное русское: "{", ".join([word for word in lst if len(word) == len(sorted(lst, key=len)[-1])]).lower()}"')




"""
Задание на автоматизацию проверки ответа API от сервера. 
Нужно написать простой тест, который проверяет JSON на правильность полей:
-Содержит все перечисленные в требованиях поля.
-Не имеет других полей.
-Все поля имеют именно тот тип, который указан в требованиях. 
Тест должен вернуть Pass или список значений, которые тест посчитал ошибочными, и причину, почему они ошибочные.
исходник: Json 15.4.2.json
"""

import json

with open('Json 15.4.2.json', encoding='utf8') as f:
    templates = json.load(f)

def CheckInt(item):
    return isinstance(item, int)

def CheckStr(item):
    return isinstance(item, str)

def CheckBool(item):
    return isinstance(item, bool)

def CheckUrl(item):
    if isinstance(item, str):
        return item.startswith('http://') or item.startswith('https://')
    else:
        return False

def CheckStrValue(item, val):
    if isinstance(item, str):
        return item in val
    else:
        return False

def ErrorLog(item, value, string):
    Error.append({item: f'{value}, {string}'})

ListOfItems = {'timestamp': 'int', 'referer': 'url', 'location': 'url',
               'remoteHost': 'str', 'partyId': 'str', 'sessionId': 'str',
               'pageViewId': 'str', 'eventType': 'val', 'item_id': 'str',
               'item_price': 'int', 'item_url': 'url', 'basket_price': 'str',
               'detectedDuplicate': 'bool', 'detectedCorruption': 'bool',
               'firstInSession': 'bool', 'userAgentName': 'str'}
Error = []
for items in templates:
    for item in items:
        if item in ListOfItems:
            if ListOfItems[item] == 'int':
                if not CheckInt(items[item]):
                    ErrorLog(item, items[item], f'ожидали тип {ListOfItems[item]}')
            elif ListOfItems[item] == 'str':
                if not CheckStr(items[item]):
                    ErrorLog(item, items[item], f'ожидали тип {ListOfItems[item]}')
            elif ListOfItems[item] == 'bool':
                if not CheckBool(items[item]):
                    ErrorLog(item, items[item], f'ожидали тип {ListOfItems[item]}')
            elif ListOfItems[item] == 'url':
                if not CheckUrl(items[item]):
                    ErrorLog(item, items[item], f'ожидали тип {ListOfItems[item]}')
            elif ListOfItems[item] == 'val':
                if not CheckStrValue(items[item], ['itemBuyEvent', 'itemViewEvent']):
                    ErrorLog(item, items[item], 'ожидали значение itemBuyEvent или itemViewEvent')
            else:
                ErrorLog(item, items[item], 'неожиданное значение')
        else:
            ErrorLog(item, items[item], 'неизвестная переменная')
if Error == []:
    print('Pass')
else:
    print('Fail')
    print(Error)

with open('Json 15.4.2_unload.json', 'w', encoding='utf8') as f:
    json.dump(templates, f, ensure_ascii=False, indent=4)

with open('Json 15.4.2_unload.json', encoding='utf8') as f:
    print(f.read())


