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
