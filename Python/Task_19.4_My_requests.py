from app.settings import valid_email, valid_password, auth_key_x
import requests
import json

# Получение ключа auth_key
def get_api_key(email: str, passwd: str):
    headers = {
        'email': email,
        'password': passwd,
    }
    res = requests.get("https://petfriends.skillfactory.ru/api/key", headers=headers)
    status = res.status_code
    try:
        result = res.json()
    except json.decoder.JSONDecodeError:
        result = res.text
    return status, result

print(get_api_key(valid_email, valid_password))


# Получение списка питомцев
def get_list_pets(auth_key: json, filter: str = "") -> json:
    headers = {'auth_key': auth_key}
    filter = {'filter': filter}
    base_url = 'https://petfriends.skillfactory.ru/'
    res = requests.get(base_url + 'api/pets', headers=headers, params=filter)
    status = res.status_code
    try:
        result = res.json()
    except:
        result = res.text
    return status, result

print(get_list_pets(auth_key_x, 'my_pets'))


# Добавление питомца без фото
def post_add_pet(auth_key: json) -> json:
    headers = {
        'auth_key': auth_key,
    }
    data = {'name': 'King-Kongs', 'animal_type': 'Monkey', 'age': 155}
    base_url = 'https://petfriends.skillfactory.ru/'
    res = requests.post(base_url + 'api/create_pet_simple', data=data, headers=headers)
    status = res.status_code
    result = res.text
    return status, result

print(post_add_pet(auth_key_x))


# Добавление питомца с фото №1
# Используем библиотеку requests_toolbelt, чтобы устранить проблему с загрузкой изображения на сервер:
from requests_toolbelt.multipart.encoder import MultipartEncoder

def add_new_petfoto1(auth_key: json, name: str, animal_type: str,
                age: str, pet_photo: str) -> json:

    data = MultipartEncoder(
        fields={
            'name': name,
            'animal_type': animal_type,
            'age': age,
            'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
        })

    headers = {'auth_key': auth_key, 'Content-Type': data.content_type}
    base_url = 'https://petfriends.skillfactory.ru/'
    res = requests.post(base_url + 'api/pets', headers=headers, data=data)
    status = res.status_code
    try:
        result = res.json()
    except json.decoder.JSONDecodeError:
        result = res.text
    return status, result

print(add_new_petfoto1(auth_key_x, name='King-Kong', animal_type='Monkey', age='1', pet_photo='images/king-kong1.jpg'))


# Добавление питомца с фото №2
def add_new_petfoto2(auth_key: json) -> json:

    headers = {
        'auth_key': auth_key,
    }
    data = {'name': 'King-Kongs', 'animal_type': 'Monkey', 'age': 155}
    files = {"pet_photo": open("images/king-kong2.jpg", "rb")}
    base_url = 'https://petfriends.skillfactory.ru/'
    res = requests.post(base_url + 'api/pets', data=data, files=files, headers=headers)
    status = res.status_code
    try:
        result = res.json()
    except json.decoder.JSONDecodeError:
        result = res.text
    return status, result

print(add_new_petfoto2(auth_key_x))


# Добавление/изменение фото
def post_add_pet_photo(auth_key: json) -> json:
    headers = {
        'auth_key': auth_key,
    }
    pet_id = '97a870a0-401e-4951-87e2-2824ef11a948'
    files = {"pet_photo": open("images/king-kong2.jpg", "rb")}
    base_url = 'https://petfriends.skillfactory.ru/'
    res = requests.post(base_url + 'api/pets/set_photo/' + pet_id, files=files, headers=headers)
    status = res.status_code
    result = res.text
    return status, result

print(post_add_pet_photo(auth_key_x))


# Изменение данных питомца
def put_add_pet(auth_key: json) -> json:
    headers = {
        'auth_key': auth_key,
    }
    data = {'name': 'Ping-Pong', 'animal_type': 'Gorila', 'age': 144}
    pet_id = '97a870a0-401e-4951-87e2-2824ef11a948'
    base_url = 'https://petfriends.skillfactory.ru/'
    res = requests.put(base_url + f'api/pets/{pet_id}', data=data, headers=headers)
    status = res.status_code
    result = res.text
    return status, result

print(put_add_pet(auth_key_x))


# Удаление питомца
def del_add_pet(auth_key: json) -> json:
    headers = {
        'auth_key': auth_key,
    }
    pet_id = '97a870a0-401e-4951-87e2-2824ef11a948'
    base_url = 'https://petfriends.skillfactory.ru/'
    res = requests.delete(base_url + f'api/pets/{pet_id}', headers=headers)
    status = res.status_code
    result = res.text
    return status, result

print(del_add_pet(auth_key_x))


