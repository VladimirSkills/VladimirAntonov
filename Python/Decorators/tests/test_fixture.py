import json
import inspect  # используем метод для возвращения имени функции
from conftest import do_repeat_it, add_file_log  # импортируем декораторы
from app.api_fixture import PetFriends
import pytest
import os

pf = PetFriends()


@pytest.mark.usefixtures("get_name_func")  # фикстура для вывода в консоли названия теста
def test_get_api_key(get_api_keys):  # в аргументе функции - фикстура для получения ключа
    """ Проверяем, что запрос ключа возвращает статус 200 и содержится слово key"""
    result = get_api_keys
    with open("out_json.json", 'w', encoding='utf8') as my_file:
        my_file.write(f'\n{inspect.currentframe().f_code.co_name}:\n')  # Выводим имя функции, как заголовок ответа
        json.dump(result, my_file, ensure_ascii=False, indent=4)
    # Сверяем полученные данные с нашими ожиданиями
    assert 'key' in result


@pytest.mark.usefixtures("get_name_func")
@do_repeat_it  # декоратор для вызова функции несколько раз
def test_add_new_pet(get_api_keys, name='King-Kong', animal_type='Monkey', age='188', pet_photo=r'../images/king-kong1.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Добавляем питомца
    status, result, content, optional = pf.add_new_pet(get_api_keys, name, animal_type, age, pet_photo)
    with open("out_json.json", 'a', encoding='utf8') as my_file:
        my_file.write(f'\n{inspect.currentframe().f_code.co_name}:\n')
        json.dump(result, my_file, ensure_ascii=False, indent=4)
    print('\nContent:', content)
    print('Optional:', optional)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name, result['animal_type'] == animal_type and result['age'] == age


@pytest.mark.usefixtures("get_name_func")
@add_file_log  # декоратор для получения ответа запроса в файл
def test_get_all_pets(get_api_keys, filter='my_pets'):
    """Проверяем, что запрос возвращает всех питомцев"""
    # Если у пользователя нет загруженных питомцев, пометим тест, как падающий через маркер xfail
    _, my_pets, _, _ = pf.get_list_of_pets(get_api_keys, "my_pets")
    if len(my_pets['pets']) == 0:
        pytest.xfail("Тест рабочий, возможно просто нет загруженных питомцев.")
    status, result, content, optional = pf.get_list_of_pets(get_api_keys, filter)
    with open("out_json.json", 'a', encoding='utf8') as my_file:
        my_file.write(f'\n{inspect.currentframe().f_code.co_name}:\n')  # Выводим имя функции, как заголовок ответа
        my_file.write(str(f'\n{status}\n{content}\n{optional}\n'))
        json.dump(result, my_file, ensure_ascii=False, indent=4)
    print('\nContent:', content)
    print('Optional:', optional)
    assert status == 200
    assert len(result['pets']) > 0


@pytest.mark.usefixtures("get_name_func")
def test_update_pet_info(get_api_keys, name='Ping-Pong', animal_type='Gorila/Monkey', age='155'):
    """Проверяем возможность обновления информации о питомце"""
    # Получаем ключ auth_key и список своих питомцев
    _, my_pets, _, _ = pf.get_list_of_pets(get_api_keys, "my_pets")
    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result, content, optional = pf.update_pet_info(get_api_keys, my_pets['pets'][0]['id'], name, animal_type, age)
        with open("out_json.json", 'a', encoding='utf8') as my_file:
            my_file.write(f'\n{inspect.currentframe().f_code.co_name}:\n')
            json.dump(result, my_file, ensure_ascii=False, indent=4)
        print('\nContent:', content)
        print('Optional:', optional)
        # Проверяем что статус ответа = 200 и новые данные питомца соответствует заданным
        assert status == 200
        assert result['name'] == name, result['animal_type'] == animal_type and result['age'] == age
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets!")


"""Тестируем создание нового питомца без фото"""
@pytest.mark.usefixtures("get_name_func")
def test_add_pet_NOfoto(get_api_keys, name='King-Bongs', animal_type='Monkey-Milk', age='122'):
    # Добавляем питомца
    status, result, content, optional = pf.add_new_pet_nofoto(get_api_keys, name, animal_type, age)
    with open("out_json.json", 'a', encoding='utf8') as my_file:
        my_file.write(f'\n{inspect.currentframe().f_code.co_name}:\n')
        json.dump(result, my_file, ensure_ascii=False, indent=4)
    print('\nContent:', content)
    print('Optional:', optional)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name, result['animal_type'] == animal_type and result['age'] == age
    assert result.get('pet_photo') == ''


@pytest.mark.usefixtures("get_name_func")
def test_add_foto_to_pet(get_api_keys, pet_photo=r'../images/king-kong2.jpg'):
    """Тестируем добавление фото к id созданного питомца без фото"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, my_pets, _, _ = pf.get_list_of_pets(get_api_keys, "my_pets")
    pet_id = my_pets['pets'][0]['id']  # id изменяемого питомца
    # Добавляем фото
    status, result, content, optional = pf.add_pet_photo(get_api_keys, pet_photo, pet_id)
    with open("out_json.json", 'a', encoding='utf8') as my_file:
        my_file.write(f'\n{inspect.currentframe().f_code.co_name}:\n')
        json.dump(result, my_file, ensure_ascii=False, indent=4)
    print('\nContent:', content)
    print('Optional:', optional)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    # Если данный текст содержится в полученном ответе, то Passed:
    assert 'data:image/jpeg' in result.get('pet_photo')


@pytest.mark.skip(reason="Путь для фото задан некорректно!")
def test_add_foto_to_pet_skip(get_api_keys, pet_photo=r'../images/king-kong44.jpg'):
    """Тестируем skip (пропуск) по какой-либо причине"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, my_pets, _, _ = pf.get_list_of_pets(get_api_keys, "my_pets")
    pet_id = my_pets['pets'][0]['id']  # id изменяемого питомца
    # Добавляем фото
    status, result, content, optional = pf.add_pet_photo(get_api_keys, pet_photo, pet_id)
    with open("out_json.json", 'a', encoding='utf8') as my_file:
        my_file.write(f'\n{inspect.currentframe().f_code.co_name}:\n')
        json.dump(result, my_file, ensure_ascii=False, indent=4)
    print('\nContent:', content)
    print('Optional:', optional)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    # Если данный текст содержится в полученном ответе, то Passed:
    assert 'data:image/jpeg' in result.get('pet_photo')


"""Тестируем изменение фото, добавленного ранее питомца"""
@pytest.mark.usefixtures("get_name_func")
def test_changes_foto(get_api_keys, pet_photo=r'../images/king-kong3.jpg'):
    # # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем список питомцев и берём id последнего добавленного
    _, my_pets, _, _ = pf.get_list_of_pets(get_api_keys, "my_pets")
    pet_id = my_pets['pets'][0]['id']  # id изменяемого питомца
    value_image1 = my_pets['pets'][0]['pet_photo']  # image изменяемой фотки
    print(f"\nvalue_image1: {len(str(value_image1))} символов: {value_image1}", sep='')
    # Добавляем фото
    status, result, content, optional = pf.add_pet_photo(get_api_keys, pet_photo, pet_id)
    value_image2 = result.get('pet_photo')
    print(f"value_image2: {len(str(value_image2))} символов: {value_image2}")
    with open("out_json.json", 'a', encoding='utf8') as my_file:
        my_file.write(f'\n{inspect.currentframe().f_code.co_name}:\n')
        json.dump(result, my_file, ensure_ascii=False, indent=4)
    print('\nContent:', content)
    print('Optional:', optional)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    # Если текст первой фотки не равен тексту второй, то Passed:
    assert value_image1 != value_image2


@pytest.mark.usefixtures("get_name_func_setup", "time_delta_teardown")
class TestDeletePets:

    """Тестируем возможность удаления одного питомца"""
    def test_delete_first_pet(self, get_api_keys):
        # Запрашиваем список своих питомцев
        _, my_pets, _, _ = pf.get_list_of_pets(get_api_keys, "my_pets")
        # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet(get_api_keys, "King-Kong", "Gorila", "133", r'../images/king-kong2.jpg')
            _, my_pets, _, _ = pf.get_list_of_pets(get_api_keys, "my_pets")
        # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        status, result, content, optional = pf.delete_pet(get_api_keys, pet_id)
        with open("out_json.json", 'a', encoding='utf8') as my_file:
            my_file.write(f'\n{inspect.currentframe().f_code.co_name}:\n')
            json.dump(result, my_file, ensure_ascii=False, indent=4)
        print('\nContent:', content)
        print('Optional:', optional)
        # Ещё раз запрашиваем список своих питомцев
        _, my_pets, _, _ = pf.get_list_of_pets(get_api_keys, "my_pets")
        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id not in my_pets.values()


    """Тестируем удаление всех питомцев"""
    def test_delete_all_pets(self, get_api_keys):
        # Получаем ключ auth_key и запрашиваем список своих питомцев
        _, my_pets, _, _ = pf.get_list_of_pets(get_api_keys, "my_pets")
        with open("out_json.json", 'a', encoding='utf8') as my_file:
            my_file.write(f'\n{inspect.currentframe().f_code.co_name}/текущий список питомцев:\n')
            json.dump(my_pets, my_file, ensure_ascii=False, indent=4)
        pet_id = my_pets['pets'][0]['id']
        # Получаем в цикле id всех питомцев из списка и отправляем запрос на удаление:
        for id_pet in my_pets["pets"]:
            pf.delete_pet(get_api_keys, id_pet["id"])
        # Ещё раз запрашиваем список питомцев:
        status, my_pets, content, optional = pf.get_list_of_pets(get_api_keys, "my_pets")
        with open("out_json.json", 'a', encoding='utf8') as my_file:
            my_file.write(f'\n{inspect.currentframe().f_code.co_name}/список после удаления:\n')
            json.dump(my_pets, my_file, ensure_ascii=False, indent=4)
        print('\nContent:', content)
        print('Optional:', optional)
        assert status == 200
        assert pet_id not in my_pets.values()

