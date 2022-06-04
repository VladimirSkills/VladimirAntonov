# Создадим виртуальное окружение в нужной папке: cd "путь".
# Ввести в Terminal: python -m venv venv
# Затем активируем его командой: venv\scripts\activate.ps1
# Установим следующие библиотека через команды:
# pip3 install pyTelegramBotAPI
# Если выйдет оповещение об обновлении, как в строке ниже, копируем её и вводим...
# c:\users\pc\pycharmprojects\vladimirantonov\python\crypto_bot\venv\scripts\python.exe -m pip install --upgrade pip
# pip3 install --upgrade pyTelegramBotAPI
# pip3 install requests
# Для выхода из venv в окне Terminal, ввести: Python.
# Команда для возврата в виртуальное окружение venv: exit()
"""МОЙ ПЕРВЫЙ БОТ"""

import telebot
from exclusions import ConvertionException, CryptoConverter
from initialdata import TOKEN, keys, countcy

bot = telebot.TeleBot(TOKEN)
# ОБРАБОТЧИКИ ДЛЯ БОТА
# Выводим первый ответ при обращении к БОТу:
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Введите данные в строчку через пробел в следующем порядке:\n> имя валюты \
\n> в какую валюту перевести \n> количество единиц валюты \
\n Посмотреть список всех доступных валют >> /values'
    bot.reply_to(message, text)

# Добавляем к обращению вывод списка валют:
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():  # выводим ключи словарей (имя валюты) через цикл
        text = '\n- '.join((text, key, ))
    bot.reply_to(message, text)

# Обрабатываем введённые пользователем данные:
# валюта1 валюта2 n / quote(котируем), base(переводим), amount(количество)
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')  # Введённым значениям назначаем переменную для обработки ошибок,
        # => получаем текст сообщения и разделяем его на список по пробелам.
        # если введено не верное кол-во параметров, чем требуется:
        if len(values) != countcy:
            raise ConvertionException('Параметры введены некорректно! См: /help')
        quote, base, amount = values  # присвоение переменных введённым значениям - values
        # Чтобы получить переменную total_base, вызываем через метод convert из класса CryptoConverter:
        total_base = CryptoConverter.convert(quote, base, amount)

        # Выводим исключения при неверном вводе или зависании сервера:
    except ConvertionException as excpt:
        bot.reply_to(message, f"Ошибка пользователя!\n{excpt}")
    except Exception as excpt:
        bot.reply_to(message, f"Не удалось обработать команду!\n{excpt}")
    else:
        #text = f'Цена {amount} {quote} в {base} = {total_base}'  # раскрасим...
        text = f'Стоимость {amount} {quote} составит {total_base} {base}'  # раскрасим...
        bot.send_message(message.chat.id, text)  # передаём сообщение пользователю

bot.polling(none_stop=True)  # Команда для запуска бота

