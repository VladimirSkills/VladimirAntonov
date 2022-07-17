from faker import Faker  # Для генерации случайного email и password для регистрации на сайте PetFriends
import logging  # Логгирование. Для вывода ответа в консоли
import requests
import json

fake = Faker()
"""
Для случайной генерации данных для регистрации, будем использовать библиотеку faker (нужно установить).
Каждый вызов метода fake.name() дает другой (случайный) результат. Это потому, что фейкер перенаправляет 
faker.Generator.method_name() вызовы на faker.Generator.format(method_name).
"""
logger = logging.getLogger("api")  # метод для вывода ответа в консоль
"""
Прописываем в файл pytest.ini (если нет, создаём) следующий код для работы метода getLogger:
[pytest]
disable_test_id_escaping_and_forfeit_all_rights_to_community_support = True
log_format = %(asctime)s %(levelname)s %(message)s
log_date_format = %Y-%m-%d %H:%M:%S
log_cli=true
log_level=INFO
"""

class RegisterUser:
    @staticmethod  # Фикстура создаёт и возвращает новый объект (см. её свойства Ctrl+Mouse). Работает в классе.
    def random():  # Функция генерирует каждый раз валидные данные
        name = fake.name()
        email = fake.email()
        password = fake.password()
        return {"name": name, "email": email, "pass": password}


class Register:
    """Выводим получение случайных данных в корень класса, чтобы использовать одни и те же данные
    для регистрации и авторизации:"""
    data = RegisterUser.random()

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def register_user(self) -> json:  # name, email, password
        res = requests.post(self.base_url + 'new_user', data=self.data)
        content = res.headers
        optional = res.request.headers
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
            logger.info(res.text)  # выводим ответ со страницы в консоль...
        return status, result, content, optional, self.data

    def authorization(self):  # email, password
        p = Register()
        data = p.data  # получаем значения: data = RegisterUser.random(), используемые для регистрации
        # Для авторизации, из data берём только значения ключей: email и pass:
        body = {'email': data['email'], 'pass': data['pass']}
        res = requests.post(self.base_url + 'login', data=body)
        content = res.headers
        optional = res.request.headers
        status = res.status_code
        url = res.request.url
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result, content, optional, body, url
