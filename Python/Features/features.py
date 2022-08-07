"""ИНТЕРЕСНЫЕ ФИШКИ ДЛЯ PYTEST"""

from conftest import do_repeat_it, add_file_log  # импортируем декораторы
from app.settings import valid_email, valid_password
import inspect  # используем метод для возвращения имени функции
import requests
import pytest
import time
import json
import os  # используем для работы с каталогами (save photo path)

"""
Скрипт для запуска конкретного теста из Terminal: python -m pytest tests/test_parametriz.py::test_triangle
tests - папка с файлами в корне проекта,
test_parametriz.py - название файла с тестами,
test_triangle - имя тест-функции.
Другие скрипты для вызова тестов и отчётов: https://docs.pytest.org/en/6.2.x/usage.html
Full pytest documentation: https://docs.pytest.org/en/7.1.x/contents.html
"""


class PetFriends:
    """Библиотека веб приложения Pet Friends"""

    def __init__(self):
        """ФИЧА-1 / шаг 1. Создаём переменную idp, чтобы можно было добавить
        фото к id именно этого созданного питомца"""
        self.idp = ""  # ФИЧА-1
        self.base_url = "https://petfriends.skillfactory.ru/"


    # Добавление питомца без фото - ФИЧА-1
    def post_add_pet_nofoto(self, auth_key: json, name: str, animal_type: str, age: str) -> json:

        headers = {'auth_key': auth_key['key']}
        data = {'name': name, 'animal_type': animal_type, 'age': age}
        res = requests.post(self.base_url + 'api/create_pet_simple', data=data, headers=headers)
        status = res.status_code
        try:
            result = res.json()
            """ФИЧА-1 / шаг 2. Передаём значение id созданного питомца в переменную idp"""
            self.idp = res.json().get("id")
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # Добавление фото к созданному питомцу без фото - ФИЧА-1
    def post_add_pet_photo(self, auth_key: json, pet_photo: str) -> json:
        headers = {'auth_key': auth_key['key']}
        """ФИЧА-1 / шаг 3. Передаём id созданного питомца(idp) в качестве параметра на добавление фото"""
        pet_id = self.idp
        files = {"pet_photo": open(pet_photo, "rb")}
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, files=files, headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result



    # Изменение фото первого питомца в списке - ФИЧА-2
    """Выносим pet_id в аргументы функции..."""
    def change_pet_photo(self, auth_key: json, pet_photo: str, pet_id: str) -> json:
        headers = {'auth_key': auth_key['key']}
        files = {"pet_photo": open(pet_photo, "rb")}
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, files=files, headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


    # Добавление питомца с фото без применения MultipartEncoder - ФИЧА-3
    # А также пример запроса на получение данных по дополнительным заголовкам - ФИЧА-4
    def add_new_pet_with_photo(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        headers = {'auth_key': auth_key['key']}
        data = {'name': name, 'animal_type': animal_type, 'age': age}
        files = {"pet_photo": open(pet_photo, "rb")}
        res = requests.post(self.base_url + 'api/pets', data=data, files=files, headers=headers)
        content = res.headers
        optional = res.request.headers
        url = res.request.url
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result, content, optional, url


"""<<<<<< Примеры ТЕСТов для запросов >>>>>>>"""

pf = PetFriends()
# Для запуска тестов нужно добавить запрос на получение ключа: pf.get_api_key (см. учебку)

"""Тестируем: Добавление фото к созданному питомцу без фото => post_add_pet_photo
Для этого теста и требовалось определение id/idp для конкретно созданного питомца - в первых двух запросах...ФИЧА-1"""
def test_post_add_petfoto(pet_photo=r'../images/king-kong1.jpg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменную auth_key
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
    print(f"value_image2: {len(value_image2)} символов: {value_image2}")
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    # Если полученное значение ключа одной картинки не равно значению ключа другой картинки - PASSED:
    assert value_image1 != value_image2


"""Тестируем: Изменение фото первого питомца в списке => change_pet_photo => ФИЧА-2"""
# Для запуска нужно в т.ч. добавить запрос на получение списка питомцев: get_list_of_pets
def test_changes_petfoto(pet_photo=r'../images/king-kong3.jpg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']  # id изменяемого питомца (первый в списке)
    value_image1 = my_pets['pets'][0]['pet_photo']  # получаем код image изменяемой фотки
    print(f"\nvalue_image1: {len(str(value_image1))} символов: {value_image1}", sep='')
    # Добавляем фото
    status, result = pf.change_pet_photo(auth_key, pet_photo, pet_id)
    value_image2 = result.get('pet_photo')  # получаем код image новой фотки
    print(f"value_image2: {len(str(value_image2))} символов: {value_image2}")
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    # Если полученное значение кода одной картинки не равно значению кода другой картинки - PASSED:
    assert value_image1 != value_image2


"""Тестируем добавление питомца с фото без применения MultipartEncoder и др...ФИЧА-3 и 4. """
def test_add_new_pet_with_photo(name='King-Kong', animal_type='Monkey', age='155', pet_photo=r'../images/king-kong3.jpg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key, _, _ = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result, content, optional, url = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    """ФИЧА-5 Вывод полученного ответа в файл. В первом тесте модуля ставим 'w', в последующих 'a'"""
    with open("out_json.json", 'w', encoding='utf8') as my_file:
        my_file.write(f'\n{inspect.currentframe().f_code.co_name}:\n')  # ФИЧА-6 Выводим имя функции, как заголовок ответа
        my_file.write(str(f'\n{status}\n{content}\n{optional}\n{url}\n'))
        json.dump(result, my_file, ensure_ascii=False, indent=4)
    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 200
    assert result['name'] == name, result['animal_type'] == animal_type and result['age'] == age
    assert 'data:image/jpeg' in result.get('pet_photo')
    assert optional.get('auth_key') == auth_key.get('key')
    assert 'api/pets' in url


"""ФИЧА-7. Тестируем возможность удаления всех питомцев пользователя"""
def test_delete_all_pets():
    # Для запуска нужно в т.ч. добавить запрос на удаление питомца: delete_pet
    # Получаем ключ auth_key и запрашиваем список питомцев пользователя:
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    with open("out_json.json", 'a', encoding='utf8') as my_file:
        my_file.write(f'\n{inspect.currentframe().f_code.co_name}/Текущий список питомцев:\n')
        json.dump(my_pets, my_file, ensure_ascii=False, indent=4)

    pet_id = my_pets['pets'][0]['id']
    # Получаем в цикле id всех питомцев из списка и отправляем запрос на удаление:
    for id_pet in my_pets["pets"]:
        pf.delete_pet(auth_key, id_pet["id"])
    # Ещё раз запрашиваем список питомцев:
    status, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    with open("out_json.json", 'a', encoding='utf8') as my_file:
        my_file.write(f'\n{inspect.currentframe().f_code.co_name}/Список после удаления:\n')
        json.dump(my_pets, my_file, ensure_ascii=False, indent=4)
    assert status == 200
    assert pet_id not in my_pets.values()



"""ФИКСТУРЫ / прописываем их в файле conftest.py (в одной папке с тестами), откуда некоторые из них
будут запускаться автоматически"""

# ФИЧА-8. Фикстура для получения ключа auth_key
# После её назначения, в запросе get_api_key не будет необходимости
@pytest.fixture()
def get_api_key_fix():
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


# ФИЧА-9. Фикстура для получения названий выполняемых тестов
# Назначается добавлением перед функций скрипта: @pytest.mark.usefixtures("get_name_func")
@pytest.fixture()
def get_name_func(request):
    print("\nНазвание теста:", request.node.name)
    yield


# ФИЧА-10. Фикстура получения времени обработки каждого теста
# Выполняется автоматически для каждого теста
@pytest.fixture(autouse=True)
def time_delta():
    start_time = time.time_ns()
    yield
    end_time = time.time_ns()
    print(f"\nВремя теста: {(end_time - start_time)//1000000}мс\n")



"""<<<<<< Примеры ТЕСТов для фикстур >>>>>>>"""

@pytest.mark.usefixtures("get_name_func")  # фикстура для вывода в консоли названия теста
def test_get_api_key(get_api_key_fix):  # в аргументе функции - фикстура для получения ключа
    result = get_api_key_fix  # вместо auth_key везде в тест-функции указываем имя фикстуры - get_api_key_fix
    # Сверяем полученные данные с нашими ожиданиями
    assert 'key' in result

# >>>Out print:
# Название теста: test_get_api_key
# PASSED [ 10%]
# Время теста: 106мс



"""ФИЧА-11. ПРИМЕР ПРИМЕНЕНИЯ ФИКСТУР ДЛЯ КЛАССА"""

# БЛОК SETUP (код, предшествующий исполнению основной функции)
# Фикстура для класса работает в паре с: @pytest.mark.usefixtures("имя фикстуры")
@pytest.fixture()  # если указать scope="class", фикстура исполнится только для первого теста в классе
# Получение названия выполняемого теста
def get_name_func_setup(request):
    print("Название теста из класса:", request.node.name)
    yield  # спец. слово, обозначающее исполняемую функцию


# БЛОК TEARDOWN (код, идущий после исполнения основной функции)
@pytest.fixture(scope="class")
# Получение времени обработки теста для класса
def time_delta_teardown(request):
    start_time = time.time_ns()
    yield
    end_time = time.time_ns()
    print(f"Время теста для класса {request.node.name}: {(end_time - start_time)//1000000}мс")

# ПРИМЕЧАНИЕ!
"""Блоки setup и teardown, в классическом представлении, используются внутри одной фикстуры:
код setup...
yield...
код teardown...
Но возможно разбить их на две фикстуры, как сделано выше... Это, как будет удобно.
"""


"""<<<<<< Примеры ТЕСТов для КЛАССОВ >>>>>>>"""
# Указыаем название фикстур для КЛАССА в аргументе глобальной фикстуры через запятую:
@pytest.mark.usefixtures("get_name_func_setup", "time_delta_teardown")
class TestDeletePets:

    """Тестируем возможность удаления одного питомца"""
    def test_delete_first_pet(self, get_api_key_fix):

    """Тестируем удаление всех питомцев"""
    def test_delete_all_pets(self, get_api_key_fix):

# >>>Out print:
# >>Название теста из класса: test_delete_first_pet PASSED[90 %]
# Время теста: 763 мс  # действует фикстура time_delta - для каждого теста, в т.ч. в классе
# >>Название теста из класса: test_delete_all_pets PASSED[100 %]
# Время теста: 1192 мс  # действует фикстура time_delta - для каждого теста, в т.ч. в классе
# >>Время теста для класса TestDeletePets: 1957 мс



"""ДЕКОРАТОРЫ / импортируются из файла: conftest.py - в котором они прописываются...
from conftest import _имя декоратора_"""

# ФИЧА-12. Теория:
def do_it_twice(func):  # создаём декоратор
   def wrapper(*args, **kwargs):  # эта функция wrapper выступает, как обёртка/шаблон для декорирования рабочей функции say_word. [*args, **kwargs] - аргументы, которые могут быть в рабочей функции, в данном случае say_word.
       # В тело функции wrapper добавляем нужный код для рабочей функции say_word - т.е. какое-то дополнение,
       # которое нужно применить к работе этой функции, при этом оно не изменит работу кода внутри самой функции say_word.
       for i in range(3):  # в данном случае мы хотим, чтобы функция say_word сработала 3 раза подряд! (или любая другая функция, для которой мы хотим применить этот декоратор)
           func(*args, **kwargs)
   return wrapper

# добавляем наш декоратор перед функцией, которую нужно декорировать (say_word) в виде синтетического сахара,
# т.е. ставим в начале знак @:
@do_it_twice
def say_word(word):  # декорируемая/рабочая функция
# тело декорируемой функции, в которой м.б. прописан любой код. В данном случае функция выводит любое указанное в ней слово.
    print(word)

say_word("Привет!")  # Вызываем нашу рабочую функцию say_word с указанием в аргументе соответствующего значения. В данном случае текста...
# >>>Out print:
# Привет! # Привет! # Привет!


# ФИЧА-12. Создаём декоратор повтора вызова функции n-раз
def do_repeat_it(func):
    def wrapper(get_api_key_fix):
        for i in range(3):
            func(get_api_key_fix)
    return wrapper

# Применяем декоратор после импортирования следующим образом:
@do_repeat_it
def test_add_new_pet(get_api_key_fix, 'и другие параметры')  # декорируемая функция


# ФИЧА-13. Декоратор получения ответа в файл для test_get_all_pets
def add_file_log(func):
    def wrapper(get_api_key_fix):
        func(get_api_key_fix)
        headers = {'auth_key': get_api_key_fix['key']}
        res = requests.get("https://petfriends.skillfactory.ru/api/pets", headers=headers,
                           params={'filter': "my_pets"})
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


# Применяем декоратор после импортирования следующим образом:
@add_file_log
def test_get_all_pets(get_api_key_fix, filter='my_pets'):



"""ПАРАМЕТРИЗАЦИЯ ТЕСТОВ PYTEST"""
# import pytest
# См. доп. примеры: https://pytest-docs-ru.readthedocs.io/ru/latest/example/index.html
# Доп. видео: https://www.youtube.com/watch?v=OVaKlTR87yk

"""ФИЧА-14. По умолчанию pytest экранирует любые не ASCII-символы,
которые используются в строках unicode для параметризации.
Например, если запустить тест для функции "python_string_slicer" используя фикстуру (см. ниже),
то на выходе получим закодированную кириллицу: u041a/u043e/u0440/..."""

# Параметризация теста с помощью фикстуры:
def python_string_slicer(str):
    if len(str) < 50 or "python" in str:
        return str
    else:
        return str[0:50]

# Функция извлекает данные из параметра фикстуры для вывода их в названии теста в консоли:
def generate_id(val):
    return "params: {0}".format(str(val))

@pytest.fixture(scope="function", params=[("Короткая строка", "Короткая строка")], ids=generate_id)
def param_fun(request):
    return request.param

def test_python_string_slicer(param_fun):
    (input, expected_output) = param_fun
    result = python_string_slicer(input)
    print("\nВходная строка: {0}\nВыходная строка: {1}\nОжидаемое значение: {2}".format(input, result, expected_output))
    assert result == expected_output

# >>> Out print:
# test_parametriz.py::test_python_string_slicer[params: ('\u041a\u043e\u0440\u043e\u0442\u043a\u0430\u044f...)] PASSED [100%]
# Входная строка: Короткая строка
# Выходная строка: Короткая строка
# Ожидаемое значение: Короткая строка

"""...Для того, чтобы использовать строки unicode в параметризации и видеть их в терминале,
как есть (без экранирования), нужно прописать в файле pytest.ini следующее:
[pytest]
disable_test_id_escaping_and_forfeit_all_rights_to_community_support = True
Сам файл pytest.ini нужно создать в папке с тестами самостоятельно.
В итоге мы получим результат теста в читабельном для кириллицы виде:
"""
# >>> Out print:
# test_parametriz.py::test_python_string_slicer[params: ('Короткая строка', 'Короткая строка')] PASSED [100%]
# ...



"""ФИЧА-15. Фикстура 'fix_api_key' (прописывается в файле: conftest.py) предназначена
для получения ключа auth_key в тестах REST API c параметризацией"""

# Для активации именно данной фикстуры, нужно атрибут 'pytest.key' указать вместо ключа auth_key в тест-функции!
@pytest.fixture(autouse=True)
def fix_api_key():
    """Фикстура для получения ключа в параметризированных тестах"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в pytest.key:
    status, pytest.key = pf.get_api_key(valid_email, valid_password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in pytest.key
    yield

"""Что это за чудо такое pytest.key? Не смог найти описание этого атрибута, но...
Это не переменная, но атрибут. Назначается он в фикстуре fix_api_key в качестве атрибута получения токена из 
API запроса: get_api_key. Если бы эта была переменная, то любое слово, годное в качестве переменной легко смогло бы 
заменить его при использовании этой переменной в тест-функциях для получения значения токена... 
Но! Нет, токен вы не получите, если будете использовать любые, отличные от атрибута pytest.key значения!
Секрет кроется в смысле фикстуры и импорта библиотеки Pytest. Получается, что атрибут key (из pytest.key) 
в нашей фикстуре fix_api_key получает значение ключа, а приставка pytest транслирует это значение через фикстуру 
в тест-функцию, где мы указываем атрибут pytest.key вместо auth_key, как это было в тестах без параметризации. 
Получается, что при параметризации, используя фикстуру для получения ключа, мы должны применять именно атрибут pytest.key.
"""

# Ниже разберём случай применения атрибута 'pytest.key' и пару новых примочек:

"""Тестируем удаление питомца по указанному ID"""

# Получаем id питомца:
# Эта функция нужна для получения валидного параметра 'pet_id' для теста удаления питомца: 'test_delete_first_pet'
def get_pet_id():
    # ФИЧА!!!: Используем переменную auth_key, так как НЕ для теста атрибут 'pytest.key' не будет работать, т.е.
    # будет получена ошибка: AttributeError: module pytest has no attribute key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets, _, _ = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    return pet_id

# ПОЗИТИВНЫЙ ТЕСТ:
@pytest.mark.parametrize("pet_id", [get_pet_id()], ids=['valid'])  # в параметрах, через функцию get_pet_id, получаем id
def test_delete_first_pet(pet_id):
    # Проверяем - если список своих питомцев пустой, пометим тест, как падающий через маркер xfail:
    _, my_pets, _, _ = pf.get_list_of_pets(pytest.key, "my_pets")  # указываем атрибут pytest.key вместо auth_key
    if len(my_pets['pets']) == 0:
        pytest.xfail("Тест рабочий, возможно просто нет загруженных питомцев.")
    # Берём id питомца из параметра и отправляем запрос на удаление:
    pytest.status, result, content, optional = pf.delete_pet(pytest.key, pet_id)
    # Ещё раз запрашиваем список своих питомцев:
    _, my_pets, _, _ = pf.get_list_of_pets(pytest.key, "my_pets")
    with open("out_json.json", 'w', encoding='utf8') as my_file:  # создаём файл out_json, куда пишем полученные ответы
        my_file.write(str(f"\n{pytest.status}\n{content}\n{optional}\nЗдесь был id питомца:'{result}'\nUser's pets:\n"))
        json.dump(my_pets, my_file, ensure_ascii=False, indent=4)
    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца:
    assert pytest.status == 200
    assert pet_id not in my_pets.values()
    # Плюс пару проверок на ответы в заголовках:
    assert 'text/html' in content.get('Content-Type')
    assert optional.get('auth_key') == pytest.key.get('key')


# НЕГАТИВНЫЕ ТЕСТЫ (образец для параметров):
@pytest.mark.parametrize("pet_id", ['', '55c01179-k2e9-41f7-81d9-d7888d47aae9', '59c011b9-d2e9-41f7-81d9-d7999d47aae9'],
                         ids=['empty', 'unexistent', 'remote'])  # and other...
def test_delete_first_pet_negative(pet_id):
    # ...




"""TESTING ON SELENIUM"""

# https://pytest-selenium.readthedocs.io/en/latest/user_guide.html
# https://habr.com/ru/company/otus/blog/596071/
# https://selenium-python.readthedocs.io/api.html

"""
Чтобы обновить Selenium или другую библиотеку, интереснее это сделать в файле requirements.txt, в котором описываются
все зависимости приложения.
Можно использовать команду: 'pip freeze > requirements.txt' в Terminal для создания/обновления файла requirements.txt.
Место установки файла - корневая директория, т.е. команду лучше запускать находясь в ней.
Доустанавливать библиотеки в файл впоследствии можно командой: 'pip install -r requirements.txt'
Библиотеки, у которых есть обновления, подчёркиваются в файле. Наводите на них мышью и появляется ссылка на обновление.
"""


"""
import logging  # Логгирование. Для вывода ответа в консоли
logger = logging.getLogger("имя запускаемого файла")  # -> для вывода ответа в консоль
Также прописываем в файл pytest.ini следующий код для работы метода getLogger:
[pytest]
disable_test_id_escaping_and_forfeit_all_rights_to_community_support = True
log_format = %(asctime)s %(levelname)s %(message)s
log_date_format = %Y-%m-%d %H:%M:%S
log_cli=true
log_level=INFO
"""


import time  # just for demo purposes, do NOT repeat it on real projects!
import win32clipboard  # для вставки из буфера (нужна установка pywin32)


def test_paste_link(selenium):
    """Тестируем Открытие видео по ссылке, копирование ссылки,
    вставку ссылки в адресную строку и воспроизведение видео"""

    # Драйвер chromedriver.exe помещаем в папку с тестом: tests
    # Запуск теста (test_paste_link) из папки, где находится тестовый файл (test_selenium.py):
    # pytest -v --driver Chrome --driver-path chromedriver.exe test_selenium.py::test_paste_link
    # Запуск теста из корня проекта. Тестовый файл находится в папке tests:
    # pytest -v --driver Chrome --driver-path tests\chromedriver.exe tests\test_selenium.py::test_paste_link

    # Открываем страницу Web: (страница теста не приводится, но код рабочий)
    selenium.get('https://.../')
    # Разворачиваем окно браузера на весь экран:
    selenium.maximize_window()
    time.sleep(1)

    # Нажимаем на скриншот видео, оно открывается в новом окне:
    selenium.find_element_by_xpath('//div[@id="widget-54966c16-d7bc-331f-85f3-5e3f9ad11460"]//img').click()

    # Активируем открывшуюся вкладку [-1] -> последняя открытая вкладка, [0] - предыдущая:
    selenium.switch_to.window(selenium.window_handles[-1])  # дескриптор последней открытой вкладки

    # Делаем скрин экрана:
    selenium.save_screenshot('open_page_video.png')
    time.sleep(1)

    # Нажимаем на кнопку Copy Link для копирования ссылки на видео:
    selenium.find_element_by_xpath('//button[@aria-label="Copy link"]').click()

    # Открываем буфер обмена:
    win32clipboard.OpenClipboard()
    # Назначаем переменной url значение в буфере:
    url = win32clipboard.GetClipboardData()
    # Открываем новую вкладку с указанием адреса из буфера обмена:
    selenium.execute_script(f"window.open('{url}', '_blank');")

    # Активируем открывшуюся вкладку / дескриптор последней открытой вкладки:
    selenium.switch_to.window(selenium.window_handles[-1])
    # Закрываем буфер обмена:
    win32clipboard.CloseClipboard()

    # Нажимаем на видео для воспроизведения:
    selenium.find_element_by_xpath('//div[@class="relative-el"]').click()
    # Нажимаем на кнопку fullscreen:
    selenium.find_element_by_xpath('//button[@class="control-bar-button video-player-fullscreen-button"]').click()
    time.sleep(10)  # чутка смотрим кино
    # Делаем скрин экрана:
    selenium.save_screenshot('video_playback.png')


    # Библиотеки для методов ниже:
    # from selenium.webdriver import ActionChains
    # from selenium.webdriver.common.keys import Keys

    # Некоторые действия с текстом: (например, для теста выше в качестве 'element' можно использовать 'selenium')
    # ActionChains(element).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()  # вставка
    # ActionChains(element).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()  # выделение
    # ActionChains(element).key_down(Keys.BACKSPACE).key_up(Keys.BACKSPACE).perform()  # удаление

    # Два варианта нажатия кнопки Enter: Keys.RETURN / Keys.ENTER
    #ActionChains(element).key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL).perform()

    # Использование TAB для перехода n-раз вперёд или назад по элементам страницы:
    # for i in range(5):
        # ActionChains(element).key_down(Keys.SHIFT).send_keys(Keys.TAB).perform()  # TAB назад
        # ActionChains(element).key_down(Keys.TAB).perform()  # TAB вперёд


"""Если к тесту добавить функцию, которая импортирует запрос к API из папки app, например: from app.api import PetFriends,
то товарищ Selenium будет ругаться:
ERROR: not found: C:\Users\PC\PycharmProjects\PySelenFix\tests\test_selenium.py::test_petfriends_signUp
(no name 'C:\\Users\\PC\\PycharmProjects\\PySelenFix\\tests\\test_selenium.py::test_petfriends_signUp' in any of [<Module test_selenium.py>])
Задачка решается добавлением пустого файла с именем: __init__.py в папку с тестами...
Это передаёт pytest, что родительский каталог папки это директория с проектом..."""



"""
Для случайной генерации данных для регистрации, можно использовать библиотеку faker (нужно установить).
Каждый вызов метода fake.name() дает другой (случайный) результат. Это потому, что фейкер перенаправляет 
faker.Generator.method_name() вызовы на faker.Generator.format(method_name).
"""
from faker import Faker  # Для генерации случайного email и password для регистрации
fake = Faker()

class RegisterUser:
    @staticmethod  # Фикстура создаёт и возвращает новый объект (см. её свойства Ctrl+Mouse). Работает в классе.
    def random():  # Функция генерирует каждый раз валидные данные
        name = fake.name()
        email = fake.email()
        password = fake.password()
        return {"name": name, "email": email, "pass": password}
        # вариант №2: return name, email, password

# примеры вызова из другой функции с классом (часть кода). Для отправки API-запроса:
data = RegisterUser.random()
res = requests.post(self.base_url + 'new_user', data=self.data)
# вариант №2 (для регистрации на сайте):
name, email, password = RegisterUser.random()



"""Работа с Cookies в Selenium тестах"""
import pickle
# Сохраняем cookie в файл cookies.pkl (после авторизации и входа на сайт) / часть кода:
with open('cookies.pkl', 'wb') as cookies:  # ('cookies.pkl', 'wb', encoding='utf8')
    pickle.dump(selenium.get_cookies(), cookies)

# Загрузка cookie на сайт для авторизации (после повторного входа):
for cookie in pickle.load(open('cookies.pkl', 'rb')):
    selenium.add_cookie(cookie)

# Обновляем страницу, куки подгружаются и происходит авторизация:
selenium.refresh()


"""Selenium WebDriver"""

"""
Тест на Selenium мы запускаем, указывая в команде запуска путь к драйверу:
Команда: pytest -v --driver Chrome --driver-path tests\chromedriver.exe tests\test_vkontakt.py::test_VK
А можно добавить импорт: from selenium import webdriver
+ Путь к драйверу: selenium = webdriver.Chrome(r'C:\Users\PC\...\chromedriver.exe')
Здесь можно также указать: selenium = webdriver.Chrome() - тоже будет работать...
И в команде не нужно будет указывать путь к драйверу:
Новая команда: pytest -v --driver Chrome tests\test_vkontakt.py::test_VK
"""


# Чтобы окно браузера (при использовании фикстуры) закрывалось также и при Failed можно, по аналогии с записью в файл,
# воспользоваться конструкцией with as:
@pytest.fixture(autouse=True)
def testing():
    with webdriver.Chrome() as driver:
        # Переходим на страницу авторизации
        driver.get('http://petfriends.skillfactory.ru/')

        yield driver
        driver.quit()

def test_show_my_pets(testing):  # фикстуру добавляем в аргумент функции
    driver = testing  # транспортируем драйвер из фикстуры
    # ... продолжение кода

"""
Явные ожидания, типа: WebDriverWait(driver, 10).until(EC.title_contains("PetFriends"))
Примеры использования методов по явным ожиданиям можно найти через поиск в Google:
В поиске указываем: "webdriverwait selenium python example title_contains" -> "title_contains" - название метода
В результатах поиска ищите сайт: https://python.hotexamples.com/... Там будут хорошие примеры по искомому методу...

Неявное ожидание -> driver.implicitly_wait(10) ->  больше применимо именно для загрузки страницы (со всеми элементами),
чем для ожидания загрузки одного элемента, на который тратится меньше секунды времени.
"""

"""
ЛОКАТОРЫ.
Трюк №5: Поиск вложенных элементов & XPath
Чтобы найти предка элемента, необходимо добавить команду ancestor::tag-name в выражение XPath. Например, выражение:
$x('//input[@type="button"]/ancestor::form') -> найдёт все формы, в которые вложен элемент input с типом button.

Для желающих открывать новое, есть хорошее решение для поиска элементов: BeautifulSoup – парсинг HTML в Python.
https://python-scripts.com/beautifulsoup-html-parsing#atribute-name-text
(См. вариант, в котором содержится текст: 'В данном примере выводится содержимое элементов, в которых есть строка 
с символами BSD' - сделайте поиск на странице по этому тексту и найдёте нужный пример кода)
"""


"""Как вставить/подгрузить картинку в Selenium"""
# Находим локатор на картинку:
get_photo = selenium.find_element(By.ID, "photo")
# Подгружаем картинку с компа:
get_photo.send_keys(r'C:\Users\PC\...\image.jpg')
