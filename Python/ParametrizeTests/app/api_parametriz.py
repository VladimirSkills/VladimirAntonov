import pytest
import requests
import json


def triangle(x, y, z):
    a, b, c = x, y, z
    side = a, b, c
    if a + b < c or a + c < b or b + c < a or min(side) <= 0 or sum(side) / 2 == max(side):
        return False
    else:
        return True


print(triangle(4, 5, 4))


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    """Часть I. Создание и получение / Add & Get => add"""

    def get_api_key(self, email: str, password: str) -> json:
        """Получаем user's key в формате json / auth_key"""

        headers = {
            'email': email,
            'password': password,
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """Получение списка питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        content = res.headers
        optional = res.request.headers
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result, content, optional

    def add_new_pet_nofoto(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Добавление питомца без фото"""
        headers = {'auth_key': auth_key['key']}  # , 'Content-Type': data.content_type}
        data = {'name': name, 'animal_type': animal_type, 'age': age}
        res = requests.post(self.base_url + 'api/create_pet_simple', data=data, headers=headers)
        content = res.headers
        optional = res.request.headers
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result, content, optional

    def add_new_pet_with_photo(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Добавление питомца с фото"""
        headers = {'auth_key': auth_key['key']}
        data = {'name': name, 'animal_type': animal_type, 'age': age}
        files = {"pet_photo": open(pet_photo, "rb")}
        res = requests.post(self.base_url + 'api/pets', data=data, files=files, headers=headers)
        content = res.headers
        optional = res.request.headers
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result, content, optional


    """Часть II. Обновление и Удаление / Change & Delete => other"""

    def add_pet_photo(self, auth_key: json, pet_photo: str, pet_id: str) -> json:
        """Добавление/изменение фото питомца"""
        headers = {'auth_key': auth_key['key']}
        files = {"pet_photo": open(pet_photo, "rb")}
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, files=files, headers=headers)
        content = res.headers
        optional = res.request.headers
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result, content, optional

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str) -> json:
        """Обновление данных питомуа по указанному ID"""
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        content = res.headers
        optional = res.request.headers
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result, content, optional

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Отправляем на сервер запрос на удаление питомца по указанному ID"""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        content = res.headers
        optional = res.request.headers
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result, content, optional
