from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
import json

class PetFriends:
    """К web приложению Pet Friends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    """ДАННЫЙ СКРИПТ ЗАМЕНЁН ФИКСТУРОЙ: @get_api_keys"""
    # def get_api_key(self, email: str, passwd: str) -> json:
    #     """Получаем user's key в формате json"""
    #
    #     headers = {'email': email, 'password': passwd}
    #     res = requests.get(self.base_url+'api/key', headers=headers)
    #     content = res.headers
    #     optional = res.request.headers
    #     status = res.status_code
    #     result = ""
    #     try:
    #         result = res.json()
    #     except json.decoder.JSONDecodeError:
    #         result = res.text
    #     return status, result, content, optional


    def get_list_of_pets(self, auth_key: json, filter: str='') -> json:
        """Получение списка питомцев"""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        content = res.headers
        optional = res.request.headers
        #cookie = res.request.headers.get('Cookie')
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result, content, optional


    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Добавляет питомца с фото"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
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
        headers = {'auth_key': auth_key['key']}  #, 'Content-Type': data.content_type}
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

