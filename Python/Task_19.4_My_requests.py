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

print(get_api_key('email', 'password'))
# # (200, {'key': '...'})


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

print(get_list_pets('указать свой', 'my_pets'))
# (200, {'pets': [{'age': '177', 'animal_type': 'Monkey', 'created_at': '...',
# 'id': '...', 'name': 'King-Kongs', 'pet_photo': 'data:image/jpeg...})


# Добавление питомца
def post_add_pet(auth_key: str):
    headers = {
        'auth_key': auth_key,
    }
    data = {'name': 'King-Kongs', 'animal_type': 'Monkey', 'age': 177}
    res = requests.post("https://petfriends.skillfactory.ru/api/create_pet_simple", data=data, headers=headers)
    status = res.status_code
    result = res.text
    return status, result

print(post_add_pet('указать свой'))
# (200, '{"_id":"","age":"177","animal_type":"Monkey","created_at":"...",
# "id":"...","name":"King-Kongs","pet_photo":"",
# "user_id":"..."}\n')


# Добавление/изменение фото
def post_add_pet_photo(auth_key: str):
    headers = {
        'auth_key': auth_key,
    }
    pet_id = 'указать свой'
    files = {"pet_photo": open("king-kong.jpg", "rb")}
    res = requests.post(f"https://petfriends.skillfactory.ru/api/pets/set_photo/{pet_id}", files=files, headers=headers)
    status = res.status_code
    result = res.text
    return status, result

print(post_add_pet_photo('указать свой'))
# (200, '{"_id":"","age":"177","animal_type":"Monkey","created_at":"...",
# "id":"...","name":"King-Kongs","pet_photo":"data:image/jpeg;...})


# Изменение данных питомца
def put_add_pet(auth_key: json) -> json:
    headers = {
        'auth_key': auth_key,
    }
    data = {'name': 'Ping-Pong', 'animal_type': 'Gorila', 'age': 144}
    pet_id = 'указать свой'
    base_url = 'https://petfriends.skillfactory.ru/'
    res = requests.put(base_url + f'api/pets/{pet_id}', data=data, headers=headers)
    status = res.status_code
    result = res.text
    return status, result

print(put_add_pet('указать свой'))
# (200, '{"age":"144","animal_type":"Gorila","created_at":"...",
# "id":"...","name":"Ping-Pong","pet_photo":"","user_id":...})


# Удаление питомца
def del_add_pet(auth_key: json) -> json:
    headers = {
        'auth_key': auth_key,
    }
    pet_id = 'указать свой'
    base_url = 'https://petfriends.skillfactory.ru/'
    res = requests.delete(base_url + f'api/pets/{pet_id}', headers=headers)
    status = res.status_code
    result = res.text
    return status, result

print(del_add_pet('указать свой'))
# (200, '')



