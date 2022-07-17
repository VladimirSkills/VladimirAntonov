import inspect  # используем метод для возвращения имени функции
from api import Register
import json


# Проверка регистрации пользователя:
def test_registration():
    # Отправляем запрос и сохраняем полученный ответ в файл: 'out_json.json':
    status, result, content, optional, data = Register().register_user()
    with open("out_json.json", 'w', encoding='utf8') as my_file:
        my_file.write(f'{inspect.currentframe().f_code.co_name}:\n')  # Выводим имя функции, как заголовок ответа
        my_file.write(str(f'\nStatus: {status}\nContent: {content}\nOptional: {optional}\nData: {data}\nResult: '))
        json.dump(result[0:result.find('<div class="card-deck">')], my_file, ensure_ascii=False, indent=4)

        """[0:result.find('<div class="card-deck">')] или [индекс 1-го символа : индекс i-го символа или слово в тексте]
        ==> выражение для получения сокращённого ответа -> с 1-го символа до атрибута: '<div class="card-deck">'. 
        Можно задать любое значение -> result.find('any_word_from_text') - для ограничения вывода текста."""
    # Сверяем полученные данные с нашими ожиданиями:
    assert status == 200
    assert 'Все питомцы наших пользователей' in result  # После регистрации, в ответе должен быть данный заголовок...
    assert 'Data is invalid' != result  # Если регистрация не прошла, будет получен этот текст...
    assert Register.data['name'] == data.get('name')
    assert Register.data['email'] == data.get('email')
    assert Register.data['pass'] == data.get('pass')


# Проверка авторизации пользователя:
def test_authorization():
    status, result, content, optional, body, url = Register().authorization()
    with open("out_json.json", 'a', encoding='utf8') as my_file:
        my_file.write(f'\n\n{inspect.currentframe().f_code.co_name}:\n')  # Выводим имя функции, как заголовок ответа
        my_file.write(str(f'\nStatus: {status}\nContent: {content}\nOptional: {optional}\nBody: {body}\nResult: '))
        json.dump(result[0:1000], my_file, ensure_ascii=False, indent=4)  # [0:1000] - указываем диапазон символов для вывода
    # Сверяем полученные данные с нашими ожиданиями:
    assert status == 200
    assert 'Все питомцы наших пользователей' in result
    assert 'all_pets' in url  # После регистрации и авторизации, мы попадаем на сайт all_pets. Затестим это...
    assert Register.data['email'] == body.get('email')
    assert Register.data['pass'] == body.get('pass')
