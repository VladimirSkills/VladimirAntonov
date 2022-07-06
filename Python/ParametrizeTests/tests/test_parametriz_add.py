import pytest
from ParametrizeTests.app.settings import valid_email, valid_password
from ParametrizeTests.app.api_parametriz import PetFriends
from ParametrizeTests.app.api_parametriz import triangle
import json
import requests
import os

pf = PetFriends()

# Тест на проверку сторон треугольника с помощью параметризации:
@pytest.mark.parametrize("x", [3, -1, 6], ids=["True", "minus", "True"])
@pytest.mark.parametrize("y", [4, 0, 5], ids=["True", "null", "True"])
@pytest.mark.parametrize("z", [5, 3, 9], ids=["True", "True", "bigval"])
def test_triangle(x, y, z):
    print("\nx: {0}, y: {1}, z: {2}".format(x, y, z))
    assert True == triangle(x, y, z)

"""Применение параметризации для тестирования различных тест-кейсов"""

def test_get_api_key():
    """ Проверяем, что запрос ключа возвращает статус 200 и содержится слово key"""
    result = pytest.key  # pytest.key - ключ из фикстуры / указать вместо ключа auth_key
    with open("out_json.json", 'w', encoding='utf8') as my_file:
        json.dump(result, my_file, ensure_ascii=False, indent=4)
    # Сверяем полученные данные с нашими ожиданиями
    assert 'key' in result


# Функции для тестов:
def generate_string(num):
    return "x" * num

def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'

def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


"""Тестируем получение данных о питомцах"""

# # ПОЗИТИВНЫЕ ТЕСТЫ
@pytest.mark.parametrize("filter", ['', 'my_pets'], ids=['empty string', 'only my pets'])
def test_get_all_pets_with_valid_key(filter):
    status, result, _, _ = pf.get_list_of_pets(pytest.key, filter)
    # Проверяем статус ответа
    assert status == 200
    assert len(result['pets']) > 0
    with open("out_json.json", 'a', encoding='utf8') as my_file:
        json.dump(result, my_file, ensure_ascii=False, indent=4)


# НЕГАТИВНЫЕ ТЕСТЫ
# @pytest.mark.parametrize("filter",
#                         [
#                             generate_string(255)
#                             , generate_string(1001)
#                             , russian_chars()
#                             , russian_chars().upper()
#                             , chinese_chars()
#                             , special_chars()
#                             , 123
#                         ],
#                         ids=
#                         [
#                             '255 symbols'
#                             , 'more than 1000 symbols'
#                             , 'russian'
#                             , 'RUSSIAN'
#                             , 'chinese'
#                             , 'specials'
#                             , 'digit'
#                         ])
# def test_get_all_pets_with_negative_filter(filter):
#     pytest.status, result, _, _ = pf.get_list_of_pets(pytest.key, filter)
#     # Проверяем статус ответа
#     assert pytest.status == 400


"""Тестируем создание нового питомца без фото"""

# ПОЗИТИВНЫЕ ТЕСТЫ
@pytest.mark.parametrize("name", ['King-Kong', generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(),
        chinese_chars(), special_chars(), '123'], ids=['valid', '255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN',
                                                       'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("animal_type", ['Gorila', generate_string(255), generate_string(1001), russian_chars(),
                                         russian_chars().upper(), chinese_chars(), special_chars(), '123'],
                ids=['valid', '255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("age", ['177', '1'], ids=['valid', 'min'])
def test_add_new_pet_simple(name, animal_type, age):
    """Проверяем, что можно добавить питомца с различными данными"""
    # Добавляем питомца
    status, result, content, optional = pf.add_new_pet_nofoto(pytest.key, name, animal_type, age)
    with open("out_json.json", 'a', encoding='utf8') as my_file:
        my_file.write(str(f'\n{status}\n{content}\n{optional}\n'))
        json.dump(result, my_file, ensure_ascii=False, indent=4)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type
    assert content.get('Content-Type') == 'application/json'
    assert optional.get('Content-Type') == 'application/x-www-form-urlencoded'


# НЕГАТИВНЫЕ ТЕСТЫ
# @pytest.mark.parametrize("name", [''], ids=['empty'])
# @pytest.mark.parametrize("animal_type", [''], ids=['empty'])
# @pytest.mark.parametrize("age", ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(),
#             russian_chars(), russian_chars().upper(), chinese_chars()], ids=['empty', 'negative', 'zero',
#             'greater than max', 'float', 'int_max', 'int_max + 1', 'specials', 'russian', 'RUSSIAN', 'chinese'])
# def test_add_new_pet_negative(name, animal_type, age):
#     """Проверяем, что можно добавить питомца с различными данными"""
#     # Добавляем питомца
#     pytest.status, result = pf.add_new_pet_nofoto(pytest.key, name, animal_type, age)
#     # Сверяем полученный ответ с ожидаемым результатом
#     assert pytest.status == 400
#     assert content.get('Content-Type') == 'text/html'



"""Тестируем создание нового питомца с фото"""

# ПОЗИТИВНЫЕ ТЕСТЫ
# @pytest.mark.parametrize("name", ['King-Kong'], ids=['valid'])
# @pytest.mark.parametrize("animal_type", ['Gorila'], ids=['valid'])
# @pytest.mark.parametrize("age", ['155'], ids=['valid'])
# Средняя проверка:
@pytest.mark.parametrize("name", ['King-Kong', '', generate_string(255), russian_chars(), '123'],
                         ids=['valid', 'empty', '255 symbols', 'russian', 'digit'])
@pytest.mark.parametrize("animal_type", ['Gorila', '', generate_string(255), russian_chars(), '123'],
                         ids=['valid', 'empty', '255 symbols', 'russian', 'digit'])
@pytest.mark.parametrize("age", ['177', '', '-1', '0', '1', '100', '1.5', chinese_chars()],
                         ids=['valid', 'empty', 'negative', 'zero', 'min', 'greater than max', 'float', 'chinese'])
@pytest.mark.parametrize("pet_photo", [r'../images/king-kong3.jpg'], ids=['valid'])
def test_add_new_pet_with_photo(name, animal_type, age, pet_photo):
    """Проверяем, что можно добавить питомца с различными данными"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Добавляем питомца
    status, result, content, optional = pf.add_new_pet_with_photo(pytest.key, name, animal_type, age, pet_photo)
    with open("out_json.json", 'a', encoding='utf8') as my_file:
        my_file.write(str(f'\n{status}\n{content}\n{optional}\n'))
        json.dump(result, my_file, ensure_ascii=False, indent=4)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result.get('name') == name and result.get('animal_type') == animal_type and result.get('age') == age
    assert 'data:image/jpeg' in result.get('pet_photo')
    assert content.get('Content-Type') == 'application/json'
    assert 'multipart/form-data' in optional.get('Content-Type')


# НЕГАТИВНЫЕ ТЕСТЫ
# @pytest.mark.parametrize("name", [''], ids=['empty'])
# @pytest.mark.parametrize("animal_type", [''], ids=['empty'])
# @pytest.mark.parametrize("age", ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(),
#             russian_chars(), russian_chars().upper(), chinese_chars()], ids=['empty', 'negative', 'zero',
#             'greater than max', 'float', 'int_max', 'int_max + 1', 'specials', 'russian', 'RUSSIAN', 'chinese'])
# @pytest.mark.parametrize("pet_photo", ['', r'../images/king-kong-err.jpg',
#                                        r'../images/king-kong4.exe', r'../images/фотоfoto.jpg'],
#                          ids=['empty', 'negative', 'exe', 'latin&cirilic'])
# def test_add_new_pet_with_photo_negative(name, animal_type, age, pet_photo):
#     """Проверяем, что можно добавить питомца с различными данными"""
#     pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
#     # Добавляем питомца
#     status, result, content, optional = pf.add_new_pet_with_photo(pytest.key, name, animal_type, age, pet_photo)
#     with open("out_json.json", 'a', encoding='utf8') as my_file:
#         my_file.write(str(f'\n{status}\n{content}\n{optional}\n'))
#         json.dump(result, my_file, ensure_ascii=False, indent=4)
#     # Сверяем полученный ответ с ожидаемым результатом
#     assert status == 403 or 500
#     assert result.get('name') == name and result.get('animal_type') == animal_type and result.get('age') == age
#     assert 'data:image/jpeg' in result.get('pet_photo')
#     assert content.get('Content-Type') == 'application/json'
#     assert 'multipart/form-data' in optional.get('Content-Type')



