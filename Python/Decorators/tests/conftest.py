"""Фикстуры и Декораторы / Set of fixtures and Decorators"""
from app.settings import valid_email, valid_password
import requests
import pytest
import time
import json


@pytest.fixture()  # scope="package"
# Получение ключа auth_key
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


@pytest.fixture()
# Получение названий выполняемых тестов
def get_name_func(request):
    print("\nНазвание теста:", request.node.name)
    yield


@pytest.fixture(autouse=True)
# Получение времени обработки каждого теста
def time_delta():
    start_time = time.time_ns()
    yield
    end_time = time.time_ns()
    print(f"\nВремя теста: {(end_time - start_time)//1000000}мс\n")


# Создаём декоратор повтора вызова функции n-раз
def do_repeat_it(func):
    def wrapper(get_api_keys):
        for i in range(3):
            func(get_api_keys)
    return wrapper


# Декоратор получения ответа в файл для test_get_all_pets
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


"""ФИКСТУРЫ ДЛЯ TEST-CLASS DELETE"""


# БЛОК SETUP:
# Фикстура для класса работает в паре с: @pytest.mark.usefixtures("имя фикстуры")
@pytest.fixture()  # если указать scope="class", фикстура исполнится только для первого теста в классе
# Получение названия выполняемого теста
def get_name_func_setup(request):
    print("Название теста из класса:", request.node.name)
    yield


# БЛОК TEARDOWN:
@pytest.fixture(scope="class")
# Получение времени обработки теста для класса
def time_delta_teardown(request):
    start_time = time.time_ns()
    yield
    end_time = time.time_ns()
    print(f"Время теста для класса {request.node.name}: {(end_time - start_time)//1000000}мс")

