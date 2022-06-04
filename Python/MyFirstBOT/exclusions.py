import json
import requests
from decimal import Decimal, ROUND_HALF_UP
from initialdata import keys

def num_format(num_x): # числовой формат:
    n = Decimal(str(num_x))
    number = n.quantize(Decimal("1.00"), ROUND_HALF_UP)  # "1.00" - здесь задаём кол-во знаков после запятой
    formi = '{0:,}'.format(number).replace(',', ' ')  # (',', ' ') - во вторых кавычках ставим нужный разделитель
    return formi

# Обработчик некорректного ввода:
class ConvertionException(Exception):  # Ошибки пользователя
    pass

# Обработку ошибок выводим в отдельный класс с применением декоратора staticmethod к функции convert,
# чтобы не перегружать работу бота:
class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:  # если введены одинаковые валюты:
            raise ConvertionException(f'Вы ввели одинаковую или некорректную валюту "{base}"!')

        # Обработка некорректного ввода имени валюты пользователем:
        try:
            quote_ticker = keys[quote]
        except KeyError:  # Ошибка по ключу
            raise ConvertionException(f'Не удалось обработать валюту "{quote}"!')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту "{base}"!')

        # Обработка некорректного ввода количества конвертируемой валюты - amount:
        try:
            amount = float(amount)
        except ValueError:  # Ошибка по значению
            raise ConvertionException(f'Не удалось обработать количество "{amount}"!')

        # вставляем с сайта запрос и делаем его динамическим, т.е. c изменяемыми переменными {код валюты по ключу}:
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = num_format(json.loads(r.content)[keys[base]] * amount)  # получаем конверт. значение
        return total_base
