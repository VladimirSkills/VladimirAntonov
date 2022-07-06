"""Фикстуры и Декораторы / Set of fixtures and Decorators"""
from ParametrizeTests.app.settings import valid_email, valid_password
from ParametrizeTests.app.api_parametriz import PetFriends
import requests
import pytest
import json

pf = PetFriends()


# Фикстура для получения ключа auth_key в тестах REST API c параметризацией
# Для активации нужно спец. переменную pytest.key указать вместо ключа auth_key в тест-функции
@pytest.fixture(autouse=True)
def fix_api_key():
    """Фикстура для получения ключа в параметризированных тестах"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, pytest.key = pf.get_api_key(valid_email, valid_password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in pytest.key
    yield


# Получение ключа auth_key
# При параметризации теста, лучше использовать фикстуру: fix_api_key
@pytest.fixture()
def get_api_keys():
    headers = {'email': valid_email, 'password': valid_password}
    res = requests.get("https://petfriends.skillfactory.ru/api/key", headers=headers)
    optional = res.request.headers
    assert optional.get('email') == valid_email
    assert optional.get('password') == valid_password
    assert res.status_code == 200
    try:
        result = res.json()
    except json.decoder.JSONDecodeError:
        result = res.text
    return result


# Декоратор получения ответа в файл для test_get_all_pets
# Имя декоратора указывается перед тест-функцией
def add_file_log(func):
    def wrapper(get_api_keys):
        func(get_api_keys)
        headers = {'auth_key': get_api_keys['key']}
        res = requests.get("https://petfriends.skillfactory.ru/api/pets", headers=headers, params={'filter': "my_pets"})
        content = res.headers
        optional = res.request.headers
        body = res.request.body
        cookie = res.cookies
        url = res.request.url
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        with open("my_log.json", 'w', encoding='utf8') as my_file:
            my_file.write(f'\nСтатус: {status}\nЗаголовки1: {content}\nЗаголовки2: {optional}\nТело запроса: '
                          f'{body}\nКуки: {cookie}\n{url}\nТело ответа:\n')
            json.dump(result, my_file, ensure_ascii=False, indent=4)
        assert res.status_code == 200
        return status, result, content, optional
    return wrapper




