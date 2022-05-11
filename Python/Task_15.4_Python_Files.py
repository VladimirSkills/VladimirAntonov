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
xfile = filename + '.' + ftype # <class 'str'> Файл txt: Testfile, из текущего каталога

# Функция для поиска самого длинного англ. слова:
def longWord(text):
    r = re.compile("([a-zA-Z]+)") # применяем регулярные выражения
    long_word = []
    for english in filter(r.match, text):
        long_word.append(english)
    return long_word

# открываем файл, читаем, приводим текст к нижнему регистру,
# убираем знаки пунктуации, получаем список слов (цифры не учитываем)
with open(xfile, encoding="utf8") as f: # , encoding="utf8"
    lst = f.read().lower().translate(
        str.maketrans('', '', '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~—')
    ).split()
# составляем словарь подсчёта
y = 3 # выводим слова длиною > y
res = {x:lst.count(x) for x in lst if len(x) > y} # по кол-ву символов в слове

print(f'Слова, длинною более {y}-х символов:')
print(f'1-ое слово: "{max(res, key=(res.get))}" - {max(res.values())} шт') # первое из наиболее часто встречающихся

#Модуль operator включает в себя функцию itemgetter(). Она возвращает значение словаря с ключом, который = 1:
sorted_res = dict(sorted(res.items(), key=operator.itemgetter(1)))
max2key = list(sorted_res.keys())[-2] # извлекаем 2-ой ключ с конца (2-ой максимум)
max2val = operator.itemgetter(max2key) # конструкция для последующего извлечения значения 2-го ключа:

print(f'2-ое слово: "{max2key}" - {max2val(sorted_res)} шт')
print(f'Самое длинное англ. слово: "{max(longWord(lst), key=len)}"')
print(f'Самое длинное русское: "{", ".join([word for word in lst if len(word) == len(sorted(lst, key=len)[-1])]).lower()}"')
