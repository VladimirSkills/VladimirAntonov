from Python.TestRequests.apirequests.settings import valid_email, valid_password, age2
from Python.TestRequests.apirequests.api import PetFriends
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result
# test_pet_friends.py::test_get_api_key_for_valid_user PASSED


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)  # статус возвращать не нужно, поэтому ставим _
    status, result = pf.get_list_of_pets(auth_key, filter)
    # # Получаем все ID питомцев:
    # print('\n', 'ID питомцев:')
    # count = 0
    # for id_pet in result["pets"]:
    #     print(id_pet["id"])
    #     count += 1
    # print(f'Всего ID: {count} шт.')

    assert status == 200
    assert len(result['pets']) > 0
# test_pet_friends.py::test_get_all_pets_with_valid_key PASSED


def test_add_new_pet_with_valid_data(name='King-Kong', animal_type='Monkey', age='188', pet_photo=r'../images/king-kong1.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)  # ????

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name, result['animal_type'] == animal_type and result['age'] == age
# test_pet_friends.py::test_add_new_pet_with_valid_data PASSED


# !!!!! Внимание, некоторые нижние проверки могут не сработать из-за отсутствия питомца...
# Временно можно закомментировать этот код.
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "King-Kong", "Gorila", "133", r'../images/king-kong2.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
# test_pet_friends.py::test_successful_delete_self_pet PASSED


def test_successful_update_self_pet_info(name='Ping-Pong', animal_type='Gorila/Monkey', age=188):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name, result['animal_type'] == animal_type and result['age'] == age
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets!")
# test_pet_friends.py::test_successful_update_self_pet_info PASSED


"""ДЕСЯТЬ ДОПОЛНИТЕЛЬНЫХ ТЕСТ-КЕЙСОВ"""


"""1. ПОЗИТИВНЫЙ. Тестируем создание нового питомца без фото"""
def test_post_add_pet_NOfoto(name='King-Bongs', animal_type='Monkey-Milk', age='122'):

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_add_pet_nofoto(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name, result['animal_type'] == animal_type and result['age'] == age
# test_pet_friends.py::test_post_add_pet_NOfoto PASSED


"""2. ПОЗИТИВНЫЙ. Тестируем добавление фото к id созданного питомца без фото"""
def test_post_add_foto_to_pet(pet_photo=r'../images/king-kong2.jpg'):

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем фото
    status, result = pf.post_add_pet_photo(auth_key, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    # print('РЕЗУЛЬТАТ>>>', result)
    assert status == 200
    # Если данный текст содержится в полученном ответе, то Passed:
    assert 'data:image/jpeg' in result.get('pet_photo')
# test_pet_friends.py::test_post_add_foto_to_pet PASSED


"""3. ПОЗИТИВНЫЙ. Тестируем изменение фото питомца"""
def test_post_changes_foto(pet_photo=r'../images/king-kong1.jpg'):

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем фото
    status, result = pf.post_add_pet_photo(auth_key, pet_photo)
    # Получаем значение картинки1:
    value_image1 = result.get('pet_photo')
    print('\n', f"value_image1: {len(value_image1)} символов: {value_image1}", sep='')

    # Добавляем новое фото:
    _, result2 = pf.post_add_pet_photo(auth_key, r'../images/king-kong3.jpg')

    # Получаем значение картинки2:
    value_image2 = result2.get('pet_photo')
    # Вариант, когда в api НЕ указываем ответ в формате json: result = res.json():
    # dict_py = json.loads(result)
    # value_image = dict_py.get('pet_photo')
    print(f"value_image2: {len(value_image2)} символов: {value_image2}")

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    # Если полученное значение ключа одной картинки не равно значению ключа другой картинки - PASSED:
    assert value_image1 != value_image2
# test_pet_friends.py::test_post_changes_foto PASSED


"""4. ПОЗИТИВНЫЙ. Тестируем передачу неверного пароля"""
def test_get_api_key_for_NOTvalid_password(email=valid_email, password="12345"):
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    print(password)

    # Сверяем полученные данные с нашими ожиданиями = 403
    assert status == 403
    assert 'key' is not result
# test_pet_friends.py::test_get_api_key_for_NOTvalid_password PASSED


"""5. ПОЗИТИВНЫЙ. Тестируем добавление фото при указании неверного ключа"""
def test_get_api_key_NOT_valid(pet_photo=r'../images/king-kong2.jpg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    auth_key = {'key': 'fs61gs651af65afg16adf51g651adfg6g165h1sF65DDF651'}

    # Добавляем фото
    status, result = pf.post_add_pet_photo(auth_key, pet_photo)
    print(auth_key)
    print(result)

    # Сверяем полученный ответ с ожидаемым результатом = 403
    assert status == 403
    assert 'Forbidden' in result
# test_pet_friends.py::test_get_api_key_NOT_valid PASSED


"""6. ПОЗИТИВНЫЙ. Тестируем удаление всех питомцев"""
def test_on_delete_all_pets():
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "King-Kong", "Gorila", "133", r'../images/king-kong2.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Сохраняем id первого питомца в списке:
    pet_id = my_pets['pets'][0]['id']
    # Получаем в цикле id всех питомцев из списка и отправляем запрос на удаление:
    for id_pet in my_pets["pets"]:
        pf.delete_pet(auth_key, id_pet["id"])

    # Ещё раз запрашиваем список своих питомцев
    status, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # print("pet_id::", pet_id)
    # print("my_pets.values::", my_pets.values())

    # Проверяем, что код = 200 и id первого питомца отсутствует в списке питомцев,
    # т.е. список должен быть пустым после удаления всех питомцев:
    assert status == 200
    assert pet_id not in my_pets.values()
# test_pet_friends.py::test_on_delete_all_pets PASSED


"""7. ПОЗИТИВНЫЙ. Тестируем код по удалению питомца без указания id."""
def test_delete_self_pet_without_id():

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "King-Kong", "Gorila", "133", r'../images/king-kong2.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = ""
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 404 и в списке питомцев нет id удалённого питомца
    print('\n', "pet_id::", pet_id)
    assert status == 404
    assert pet_id not in my_pets.values()
# test_pet_friends.py::test_delete_self_pet_without_id PASSED


"""8. НЕГАТИВНЫЙ. Тестируем добавление фото с неверным указанием расширения. Верно: jpg"""
def test_post_add_NoneFoto_to_pet(pet_photo=r'../images/king-kong2.jpeg'):

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем фото
    status, result = pf.post_add_pet_photo(auth_key, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    #print('РЕЗУЛЬТАТ>>>', result)
    assert status == 200
    # Если данный текст содержится в полученном ответе, то Passed:
    assert 'data:image/jpeg' in result.get('pet_photo')
# test_pet_friends.py::test_post_add_NoneFoto_to_pet FAILED


"""9. НЕГАТИВНЫЙ. Тестируем передачу не всех параметров в запросе"""
def test_post_add_pet_NOTvalid_param(name='King-Bongs', age='122'):

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_add_pet_nofoto(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name, result['animal_type'] == animal_type and result['age'] == age
# test_pet_friends.py::test_post_add_pet_NOTvalid_param FAILED


"""10. НЕГАТИВНЫЙ. Тестируем добавление большого значения
(в т.ч. экспоненциальное = 3.138886636534116e+73)
через параметр возраст. В переменной age2 - 2368 цифры."""
def test_big_value_age_update(name='King-Long', animal_type='Gorila-BigAge', age=age2):
    """НЕ СМОТРЯ НА ЧИСЛОВОЙ ТИП age, ДАННЫЕ ПЕРЕДАЮТСЯ И В СТРОКОВОМ ФОРМАТЕ"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем, если статус ответа = 200 и длину возраста более 3 цифр принимает,
        # значит тест проходит с очень большим значением, чего быть не должно:
        assert status == 200
        assert len(result['age']) > 3
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets!")
# test_pet_friends.py::test_big_value_age_update PASSED

