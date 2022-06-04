# Токен, полученный при регистрации БОТа в Telegramm через BotFather:
TOKEN = "ввести token Telegram"

# Список валют:
keys = {
    'рубль': 'RUB',
    'доллар': 'USD',
    'евро': 'EUR'
}

# подсчёт кол-ва единиц валюты:
countcy = 0
for key in keys.keys():
    countcy += 1
