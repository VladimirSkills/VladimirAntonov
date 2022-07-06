import pytest
from ParametrizeTests.app.settings import valid_email, valid_password
from ParametrizeTests.app.api_parametriz import PetFriends
import json
import requests
import os

pf = PetFriends()


# Функции для тестов:
def generate_string(num):
    return "x" * num

def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'

def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


"""Тестируем добавление/изменение фото питомца"""

# ПОЗИТИВНЫЕ ТЕСТЫ
@pytest.mark.parametrize("pet_photo", [r'../images/king-kong2.jpg'], ids=['valid'])
def test_add_photo_to_pet(pet_photo):
    # Добавляем питомца без фото:
    _, result, _, _ = pf.add_new_pet_nofoto(pytest.key, "King-Kong", "Gorila", "133")
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, my_pets, _, _ = pf.get_list_of_pets(pytest.key, "my_pets")
    pet_id = my_pets['pets'][0]['id']  # id изменяемого питомца
    # Добавляем фото
    status, result, content, optional = pf.add_pet_photo(pytest.key, pet_photo, pet_id)
    with open("out_json.json", 'w', encoding='utf8') as my_file:
        my_file.write(str(f'\n{status}\n{content}\n{optional}\n'))
        json.dump(result, my_file, ensure_ascii=False, indent=4)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    # Если данный текст содержится в полученном ответе, то Passed:
    assert 'data:image/jpeg' in result.get('pet_photo')
    assert content.get('Content-Type') == 'application/json'
    assert 'multipart/form-data' in optional.get('Content-Type')


# НЕГАТИВНЫЕ ТЕСТЫ
# @pytest.mark.parametrize("pet_photo", ['', r'../images/king-kong-err.jpg',
#                                        r'../images/king-kong4.exe', r'../images/фотоfoto.jpg'],
#                          ids=['empty', 'negative', 'exe', 'latin&cirilic'])
# def test_add_photo_to_pet_negative(pet_photo):
#     # Добавляем питомца без фото:
#     _, result, _, _ = pf.add_new_pet_nofoto(pytest.key, "King-Kong", "Gorila", "133")
#     # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
#     pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
#     _, my_pets, _, _ = pf.get_list_of_pets(pytest.key, "my_pets")
#     pet_id = my_pets['pets'][0]['id']  # id изменяемого питомца
#     # Добавляем фото
#     status, result, content, optional = pf.add_pet_photo(pytest.key, pet_photo, pet_id)
#     with open("out_json.json", 'w', encoding='utf8') as my_file:
#         my_file.write(str(f'\n{status}\n{content}\n{optional}\n'))
#         json.dump(result, my_file, ensure_ascii=False, indent=4)
#     # Сверяем полученный ответ с ожидаемым результатом
#     assert status == 500
#     # Если данный текст содержится в полученном ответе, то Passed:
#     assert 'data:image/jpeg' in result.get('pet_photo')
#     assert content.get('Content-Type') == 'application/json'
#     assert 'multipart/form-data' in optional.get('Content-Type')


"""Тестируем обновление данных питомца по указанному ID"""

# ПОЗИТИВНЫЕ ТЕСТЫ
@pytest.mark.parametrize("name", ['Kong, King-Kong'], ids=['valid'])
@pytest.mark.parametrize("animal_type", ['Gorila-Monkey'], ids=['valid'])
@pytest.mark.parametrize("age", ['144'], ids=['valid'])
def test_update_pet_info(name, animal_type, age):
    _, my_pets, _, _ = pf.get_list_of_pets(pytest.key, "my_pets")
    # Если список не пустой, то пробуем обновить у созданного питомца его данные:
    if len(my_pets['pets']) > 0:
        status, result, content, optional = pf.update_pet_info(pytest.key, my_pets['pets'][0]['id'], name, animal_type, age)
        with open("out_json.json", 'w', encoding='utf8') as my_file:
            my_file.write(str(f'\n{status}\n{content}\n{optional}\n'))
            json.dump(result, my_file, ensure_ascii=False, indent=4)
        # Проверяем статус ответа и что тело запроса соответствует заданному:
        assert status == 200
        assert result.get('name') == name and result.get('animal_type') == animal_type and result.get('age') == age
        assert content.get('Content-Type') == 'application/json'
        assert 'application/x-www-form-urlencoded' in optional.get('Content-Type')
    else:
        # Если список пустой, то выводим сообщение:
        assert len(my_pets['pets']) == 0
        raise Exception("There is no user pets!")


# НЕГАТИВНЫЕ ТЕСТЫ
# @pytest.mark.parametrize("name", [''], ids=['empty'])
# @pytest.mark.parametrize("animal_type", [''], ids=['empty'])
# @pytest.mark.parametrize("age", [''], ids=['empty'])
# def test_update_pet_info_negative(name, animal_type, age):
#     _, my_pets, _, _ = pf.get_list_of_pets(pytest.key, "my_pets")
#     # Если список не пустой, то пробуем обновить у созданного питомца его данные:
#     if len(my_pets['pets']) > 0:
#         status, result, content, optional = pf.update_pet_info(pytest.key, my_pets['pets'][0]['id'], name, animal_type, age)
#         with open("out_json.json", 'w', encoding='utf8') as my_file:
#             my_file.write(str(f'\n{status}\n{content}\n{optional}\n'))
#             json.dump(result, my_file, ensure_ascii=False, indent=4)
#         # Проверяем статус ответа и что тело запроса соответствует заданному:
#         assert status == 200
#         assert result.get('name') == name and result.get('animal_type') == animal_type and result.get('age') == age
#         assert content.get('Content-Type') == 'application/json'
#         assert 'application/x-www-form-urlencoded' in optional.get('Content-Type')
#     else:
#         # Если список пустой, то выводим сообщение:
#         assert len(my_pets['pets']) == 0
#         raise Exception("There is no user pets!")



"""Тестируем удаление питомца по указанному ID"""

# Получаем id питомца:
def get_pet_id():
    # Используем переменную auth_key, так как НЕ для теста атрибут pytest.key не будет валидным:
    # AttributeError: module pytest has no attribute key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets, _, _ = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    return pet_id

# ПОЗИТИВНЫЕ ТЕСТЫ
@pytest.mark.parametrize("pet_id", [get_pet_id()], ids=['valid'])
def test_delete_first_pet(pet_id):
    # Проверяем - если список своих питомцев пустой, пометим тест, как падающий через маркер xfail:
    _, my_pets, _, _ = pf.get_list_of_pets(pytest.key, "my_pets")
    if len(my_pets['pets']) == 0:
        pytest.xfail("Тест рабочий, возможно просто нет загруженных питомцев.")
    # Берём id первого питомца из списка и отправляем запрос на удаление
    status, result, content, optional = pf.delete_pet(pytest.key, pet_id)
    with open("out_json.json", 'w', encoding='utf8') as my_file:
        my_file.write(str(f'\n{status}\n{content}\n{optional}\n'))
        json.dump(result, my_file, ensure_ascii=False, indent=4)
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets, _, _ = pf.get_list_of_pets(pytest.key, "my_pets")
    print(pet_id)
    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
    assert 'text/html' in content.get('Content-Type')
    assert optional.get('auth_key') == pytest.key.get('key')


# НЕГАТИВНЫЕ ТЕСТЫ
@pytest.mark.parametrize("pet_id", ['', '55c01179-k2e9-41f7-81d9-d7888d47aae9', '59c011b9-d2e9-41f7-81d9-d7999d47aae9'],
                         ids=['empty', 'unexistent', 'remote'])
def test_delete_first_pet_negative(pet_id):
    # Проверяем - если список своих питомцев пустой, пометим тест, как падающий через маркер xfail:
    _, my_pets, _, _ = pf.get_list_of_pets(pytest.key, "my_pets")
    if len(my_pets['pets']) == 0:
        pytest.xfail("Тест рабочий, возможно просто нет загруженных питомцев.")
    # Берём id первого питомца из списка и отправляем запрос на удаление
    status, result, content, optional = pf.delete_pet(pytest.key, pet_id)
    with open("out_json.json", 'w', encoding='utf8') as my_file:
        my_file.write(str(f'\n{status}\n{content}\n{optional}\n'))
        json.dump(result, my_file, ensure_ascii=False, indent=4)
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets, _, _ = pf.get_list_of_pets(pytest.key, "my_pets")
    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 404
    assert pet_id not in my_pets.values()
    assert 'text/html' in content.get('Content-Type')
    assert optional.get('auth_key') == pytest.key.get('key')



