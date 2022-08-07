#!/usr/bin/python3
# -*- encoding=utf8 -*-
# coding=utf-8

import pytest
from api2 import PetFriends  # для работы нужно в папку с тестом добавить пустой файл: __init__.py
from file_x import email, password
from faker import Faker  # Для генерации случайного email и password
from selenium import webdriver  # подключение библиотеки
from selenium.webdriver.support.ui import WebDriverWait  # Для применения явных ожиданий
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By  # Для применения локаторов
from selenium.webdriver import ActionChains  # Для симуляции нажатия клавиш на клавиатуре
from selenium.webdriver.common.keys import Keys  # Для симуляции нажатия клавиш на клавиатуре
import win32clipboard  # для вставки из буфера (нужна установка pywin32)
import pickle  # Для работы с cookies
import time  # time.sleep(сек) - В данных тестах, используется для демонстрации. Обычно применяется явное и неявное ожидание.
import os  # для работы с путями к файлам


"""
Написать тест, который проверяет, что на странице со списком питомцев пользователя:
Присутствуют все питомцы.
Хотя бы у половины питомцев есть фото.
У всех питомцев есть имя, возраст и порода.
У всех питомцев разные имена.
В списке нет повторяющихся питомцев. 
В написанном тесте добавьте неявные ожидания всех элементов (фото, имя питомца, его возраст),
добавьте явные ожидания элементов страницы.
"""

@pytest.fixture(autouse=True, scope="session")
def testing_find_element():  # browser
    with webdriver.Chrome() as driver:  # with - закрывает браузер в т.ч. при ошибке
        #driver = webdriver.Chrome()
        driver.implicitly_wait(5)  # установка Неявного ожидания
        # Переходим на страницу авторизации
        driver.get('http://petfriends.skillfactory.ru/login')
        driver.maximize_window()

        yield driver

        # Нажать на кнопку Выйти
        driver.find_element(By.XPATH, "//button[@onclick=\"document.location='/logout';\"]").click()
        driver.implicitly_wait(3)  # Установка Неявного ожидания
        # После выхода, ждём открытие страницы с Регистрацией
        driver.find_element(By.XPATH, '//button[contains(text(), "Зарегистрироваться")]')
        # Делаем скрин экрана:
        driver.save_screenshot('outscreen.png')
        driver.quit()


# pytest -v --driver Chrome test_search_element.py::test_find_element_my_pets
def test_find_element_my_pets(testing_find_element):
    driver = testing_find_element  # транспортируем драйвер
    # Активируем ожидание пока не загрузится страница авторизации:
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//label[@for='email']")))
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Активируем ожидание пока не загрузится главная страница:
    WebDriverWait(driver, 5).until(EC.title_contains("PetFriends"))
    # Нажимаем на кнопку Мои питомцы
    driver.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click()

    # Активируем ожидание пока не загрузится страница Мои питомцы:
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]')))

    # Установка Неявного ожидания на кнопку Выйти:
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH, "//button[@onclick=\"document.location='/logout';\"]")

    # Находим всех питомцев
    driver.implicitly_wait(2)  # установка Неявного ожидания
    pets = driver.find_elements(By.XPATH, '//th[@scope="row"]')
    # Содержание статистики пользователя
    statistic_user = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]')
    # Находим всех без фото
    no_images = driver.find_elements(By.XPATH, '//img[@src=""]')
    # Находим все теги img
    img = driver.find_elements(By.CSS_SELECTOR, 'th[scope="row"] img')
    # Кол-во питомцев с фото
    have_images = (len(img) - len(no_images))
    # Находим локатор для извлечения Имени, Породы, Возраста
    pet_information = driver.find_elements(By.XPATH, '//text()/ancestor::td')
    # Локатор для имени
    driver.implicitly_wait(2)  # установка Неявного ожидания
    names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]//td[1]')
    names_list = [x.text for x in names]  # Создаём список имён
    print('\nСписок Имён:', names_list)
    names_unique = list(set(names_list))  # поиск уникальных имён
    print('Уникальные Имена:', names_unique)
    # Локатор для профиля питомца:
    driver.implicitly_wait(2)  # установка Неявного ожидания
    pet_profile = driver.find_elements(By.XPATH, '//td/ancestor::tr')
    pet_profile_list = [x.text for x in pet_profile]  # Создаём список профилей
    print('Список профилей:', pet_profile_list)
    pet_profile_unique = list(set(pet_profile_list))  # поиск уникальных профилей
    print('Уникальные Профили:', pet_profile_unique)

    # 1.Проверяем, что присутствуют все питомцы / через str:
    assert str(len(pets)) in statistic_user.text
    # Также можно сделать сравнение числа с числом через извлечение числа из текста / int:
    assert len(pets) == int(statistic_user.text.split()[2])
    print('Статистика пользователя:', statistic_user.text.split())
    print('Всего питомцев:', statistic_user.text.split()[2])  # число
    # 2.Проверяем, что хотя бы у половины питомцев есть фото:
    assert have_images >= len(pets) * 0.5
    print(f"Есть фото: {have_images}")
    # 3.Проверяем, что у всех питомцев есть имя, возраст и порода через цикл:
    for i in range(len(pet_information)):
        assert pet_information[i].text != ''
    # 4.Проверяем, что у всех питомцев разные имена:
    assert len(names_list) != len(names_unique)  # длина списка совпадает с кол-вом уникальных
    # 5.Проверяем, что в списке нет повторяющихся питомцев:
    assert len(pet_profile_list) != len(pet_profile_unique)  # длина списка совпадает с кол-вом уникальных



"""Тестируем Открытие видео по ссылке, копирование ссылки,
вставку ссылки в адресную строку и воспроизведение видео"""
def test_paste_link(selenium):
    # Запуск теста (test_paste_link) из папки, где находится тестовый файл (test_selenium.py):
    # pytest -v --driver Chrome --driver-path chromedriver.exe test_selenium.py::test_paste_link

    # Открываем страницу Web:
    selenium.get('https://antonov21vek.ru/')
    # Разворачиваем окно браузера на весь экран:
    selenium.maximize_window()
    time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

    # Нажимаем на скриншот видео, оно открывается в новом окне:
    selenium.find_element(By.XPATH, '//div[@id="widget-54966c16-d7bc-331f-85f3-5e3f9ad11460"]//img').click()

    # Активируем открывшуюся вкладку [-1] -> последняя открытая вкладка, [0] - предыдущая:
    selenium.switch_to.window(selenium.window_handles[-1])  # дескриптор последней открытой вкладки

    # Делаем скрин экрана:
    selenium.save_screenshot('open_page_video.png')
    time.sleep(1)

    # Нажимаем на кнопку Copy Link для копирования ссылки на видео:
    selenium.find_element(By.XPATH, '//button[@aria-label="Copy link"]').click()
    time.sleep(1)

    # Открываем буфер обмена:
    win32clipboard.OpenClipboard()
    # Назначаем переменной url значение в буфере:
    url = win32clipboard.GetClipboardData()
    # Открываем новую вкладку с указанием адреса из буфера обмена:
    selenium.execute_script(f"window.open('{url}', '_blank');")
    time.sleep(1)
    # Активируем открывшуюся вкладку / дескриптор последней открытой вкладки:
    selenium.switch_to.window(selenium.window_handles[-1])
    # Закрываем буфер обмена:
    win32clipboard.CloseClipboard()
    time.sleep(1)

    # Нажимаем на видео для воспроизведения:
    selenium.find_element(By.XPATH, '//div[@class="relative-el"]').click()
    # Нажимаем на кнопку fullscreen:
    selenium.find_element(By.XPATH, '//button[@class="control-bar-button video-player-fullscreen-button"]').click()
    time.sleep(10)  # чутка смотрим кино
    # Делаем скрин экрана:
    selenium.save_screenshot('video_playback.png')

    ## Некоторые действия с текстом: (для теста выше в качестве 'element' используется 'selenium')
    # ActionChains(selenium).key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()  # копирование
    # ActionChains(element).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()  # вставка
    # ActionChains(element).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()  # выделение
    # ActionChains(element).key_down(Keys.BACKSPACE).key_up(Keys.BACKSPACE).perform()  # удаление

    ## Два варианта нажатия кнопки Enter: Keys.RETURN / Keys.ENTER
    # ActionChains(element).key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL).perform()

    ## Использование TAB для перехода n-раз вперёд или назад по элементам страницы:
    # for i in range(5):
        # ActionChains(element).key_down(Keys.SHIFT).send_keys(Keys.TAB).perform()  # TAB назад
        # ActionChains(element).key_down(Keys.TAB).perform()  # TAB вперёд



"""
Если к тесту добавить функцию, которая импортирует запрос к API из папки app, например: from app.api import PetFriends,
то Selenium будет ругаться.
Задачка решается добавлением пустого файла с именем: __init__.py в папку с те-стами... 
Это передаёт pytest, что родительский каталог папки это директория с проектом.
"""

"""Тестирование РЕГИСТРАЦИИ и добавления элементов через веб-интерфейс"""

# Запуск теста из папки проекта.
# pytest -v --driver Chrome --driver-path tests\chromedriver.exe tests\test_selenium.py::test_petfriends_signUp

fake = Faker()

class RegisterUser:
    @staticmethod  # Фикстура создаёт и возвращает новый объект (см. её свойства Ctrl+Mouse). Работает в классе.
    def random():  # Функция генерирует каждый раз валидные данные
        name = fake.name()
        email = fake.email()
        password = fake.password()
        return name, email, password


def test_petfriends_signUp(selenium):

    name, email, password = RegisterUser.random()
    # Открыть страницу PetFriends:
    selenium.get("https://petfriends.skillfactory.ru/")
    time.sleep(2)
    # Разворот окна браузера на весь экран:
    selenium.maximize_window()
    time.sleep(2)
    # Нажать на кнопку Регистрация.
    selenium.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]").click()
    time.sleep(1)
    # Поиск поля, очищение и ввод имени пользователя.
    a = selenium.find_element(By.ID, "name")
    a.clear()
    a.send_keys(name)
    time.sleep(2)
    # Поиск поля, очищение и ввод email пользователя.
    b = selenium.find_element(By.ID, "email")
    b.clear()
    b.send_keys(email)
    time.sleep(2)
    # Поиск поля, очищение и ввод password пользователя.
    c = selenium.find_element(By.ID, "pass")
    c.clear()
    c.send_keys(password)
    time.sleep(2)

    # Нажать на кнопку Регистрация.
    selenium.find_element(By.XPATH, '//button[@class="btn btn-success"]').click()
    time.sleep(4)
    # Нажать на кнопку Мои питомцы
    selenium.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click()
    time.sleep(2)

    # Проверяем, что мы на нужной странице:
    assert selenium.current_url == 'https://petfriends.skillfactory.ru/my_pets'

    # Нажать на кнопку Добавить питомца.
    selenium.find_element(By.XPATH, '//button[@class="btn btn-outline-success"]').click()
    time.sleep(2)
    # В открытом модальном окне добавить:
    # Фото
    pet_photo = selenium.find_element(By.ID, "photo")
    pet_photo.send_keys(r'C:\Users\PC\PycharmProjects\PySelenFix\images\king-kong2.jpg')
    time.sleep(2)
    # Имя:
    name_pet = selenium.find_element(By.XPATH, '//input[@id="name"]')
    name_pet.clear()
    name_pet.send_keys('Горилка')
    time.sleep(2)
    # Породу
    type_pet = selenium.find_element(By.XPATH, '//input[@id="animal_type"]')
    type_pet.clear()
    type_pet.send_keys('Обезьянка')
    time.sleep(2)
    # Возраст
    age_pet = selenium.find_element(By.XPATH, '//input[@id="age"]')
    age_pet.clear()
    age_pet.send_keys('12')
    time.sleep(2)
    # Нажать на кнопку Добавить:
    selenium.find_element(By.XPATH, '//button[@onclick="add_pet();"]').click()
    time.sleep(3)

    images = selenium.find_elements(By.CSS_SELECTOR, 'th[scope="row"] img')
    names = selenium.find_elements(By.XPATH, '//*[@id="all_my_pets"]//td[1]')

    # Проверяем, что питомец добавлен или нет незаполненных элементов:
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''

    # Другой вариант добавления фото - №2 - через API запрос к серверу в папке api2:
    # def test_add_foto(pet_photo=r'../images/king-kong1.jpg'):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    #     _, auth_key = PetFriends().get_api_key(email, password)
    #     _, my_pets = PetFriends().get_list_of_pets(auth_key, "my_pets")
    #     pet_id = my_pets['pets'][0]['id']
    #     status, result = PetFriends().post_add_pet_photo(auth_key, pet_id, pet_photo)
    #     # with open("out_json.json", 'w', encoding='utf8') as my_file:
    #     #     json.dump(result, my_file, ensure_ascii=False, indent=4)
    #     assert status == 200
    #     assert 'data:image/jpeg' in result.get('pet_photo')
    #     assert my_pets['pets'][0]['id'] in result.get('id')
    #     return test_add_foto
    # test_add_foto()
    # # Обновить страницу (должно появится фото)
    # selenium.refresh()
    # time.sleep(4)


    # Нажать на крестик "Удалить питомца":
    for i in range(len(names)):
        selenium.find_element(By.XPATH, '//div[@title="Удалить питомца"]').click()
    selenium.refresh()  # Обновляемся для обновления счётчика питомцев в статике user
    time.sleep(2)
    # Проверяем, что питомцев нет / при использовании варианта №2:
    # _, auth_key = PetFriends().get_api_key(email, password)
    # _, my_pets = PetFriends().get_list_of_pets(auth_key, "my_pets")
    # assert my_pets['pets'] == []

    # Содержание статистики пользователя
    statistic_user = selenium.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]')
    lists = statistic_user.text.split()  # Получаем текст статистики в виде списка
    item = '0'
    index = lists.index(item)  # Ищем индекс первого вхождения нуля, так как кол-во питомцев указано в начале
    # Проверяем, что питомцев нет
    assert int(statistic_user.text.split()[index]) == 0

    # Нажать на кнопку Выйти
    selenium.find_element(By.XPATH, "//button[@onclick=\"document.location='/logout';\"]").click()
    time.sleep(3)



"""
АВТОРИЗАЦИЯ на сайте с помощью Cookies
Приведён только код теста!
"""
# pytest -v --driver Chrome tests/test_PetFriendsCookie.py::test_cookie_petfriends
def test_cookie_petfriends(web_browser):
    # Авторизация:
    page = AuthPage(web_browser)
    # В файле auth_page class AuthPage обозначены сайт и скрипты для локаторов
    # web_browser - фикстура в файле conftest.py
    page.email.send_keys(email)
    page.password.send_keys(password)
    page.btn.click()
    time.sleep(2)

    # Сохраняем cookie в файл cookies.txt
    with open('cookies.txt', 'wb') as cookies:
        pickle.dump(web_browser.get_cookies(), cookies)

    # Цепляем заголовки в файл (для эксперимента):
    headers = web_browser.execute_script(
    "var req = new XMLHttpRequest();req.open('GET', document.location, false);req.send(null);return req.getAllResponseHeaders()")
    headers = headers.splitlines()
    with open("HeadersFile.txt", 'w', encoding='utf8') as my_file:
        my_file.write(str(headers))

    page.go_out.click()  # выходим с сайта, нажимая на кнопку Выйти
    time.sleep(2)

    # Заходим снова на сайт:
    web_browser.get('https://petfriends.skillfactory.ru')
    web_browser.maximize_window()
    time.sleep(3)

    # Загружаем cookie
    for cookie in pickle.load(open('cookies.txt', 'rb')):
        web_browser.add_cookie(cookie)

    web_browser.refresh()  # обновляем страницу и авторизуемся...
    time.sleep(3)

    # Делаем скриншот, что мы там были ))
    web_browser.save_screenshot('All pets.png')
    # Ну и проверяем...
    assert page.get_current_url() == 'https://petfriends.skillfactory.ru/all_pets'




"""Сделал парсинг-тест студентам
для разбора примера проверки наличия элементов в карточках, загруженных пользователями..."""

"""Команда для запуска, если chromedriver.exe находится в папке с тестом и путь в Terminal также к этой папке указан:
pytest -v --driver Chrome --driver-path chromedriver.exe test_ВАШЕ ИМЯ.py::test_show_my_pets
Данный тест, можно запустить и через Run (только закомитьте другие тесты в файле)"""


@pytest.fixture(autouse=True)
def browser():
    with webdriver.Chrome() as driver:  # with - закрывает браузер в т.ч. при ошибке
        # Переходим на страницу авторизации
        driver.get('http://petfriends.skillfactory.ru/login')

        yield driver
        driver.quit()


def test_show_my_pets(browser):  # фикстуру добавляем в аргумент функции
    driver = browser  # транспортируем драйвер из фикстуры
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)
    time.sleep(2)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    time.sleep(2)

    """
    Мы объявили три переменные, в которых записали все найденные элементы на странице:
    в images — все картинки питомцев, в names — все их имена, в descriptions — все виды и возрасты.
    """
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''  # на странице нет питомцев без фото
        assert names[i].text != ''  # на странице нет питомцев без Имени
        assert descriptions[i].text != ''  # на странице нет питомцев с пустым полем для указания Породы и возраста
        assert ', ' in descriptions[i]  # проверяем, что между породой и лет есть запятая (значит есть оба значения)
        parts = descriptions[i].text.split(", ")  # Создаём список, где разделитель значений - запятая
        assert len(parts[0]) > 0  # Проверяем, что длина текста в первой части списка и
        assert len(parts[1]) > 0  # ...и во второй > 0, значит там что-то да указано! Если нет -> FAILED!

    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"  # проверка, что мы были на главной странице
    # есть утверждение для проверки заголовка страницы, что <title> Label содержит текст «PetFriends»:
    assert 'PetFriends' in driver.title
