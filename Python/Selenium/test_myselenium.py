#!/usr/bin/python3
# -*- encoding=utf8 -*-
# coding=utf-8

import pytest
from app.file_x import email, password
from selenium import webdriver  # подключение библиотеки
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture(autouse=True)
def testing_find_element():
    with webdriver.Chrome() as driver:  # with - закрывает браузер в т.ч. при ошибке
        #driver = webdriver.Chrome()
        driver.implicitly_wait(5)  # установка Неявного ожидания
        # Переходим на страницу авторизации
        driver.get('http://petfriends.skillfactory.ru/login')
        driver.maximize_window()

        yield driver

        # Нажать на кнопку Выйти
        driver.find_element_by_xpath("//button[@onclick=\"document.location='/logout';\"]").click()
        driver.implicitly_wait(3)  # Установка Неявного ожидания
        # После выхода, ждём открытие страницы с Регистрацией
        driver.find_element_by_xpath('//button[contains(text(), "Зарегистрироваться")]')
        # Делаем скрин экрана:
        driver.save_screenshot('outscreen.png')
        driver.quit()


def test_find_element_my_pets(testing_find_element):
    driver = testing_find_element  # транспортируем драйвер
    # Активируем ожидание пока не загрузится страница авторизации:
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//label[@for='email']")))
    # Вводим email
    driver.find_element_by_id('email').send_keys(email)
    # Вводим пароль
    driver.find_element_by_id('pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element_by_css_selector('button[type="submit"]').click()

    # Активируем ожидание пока не загрузится главная страница:
    WebDriverWait(driver, 5).until(EC.title_contains("PetFriends"))
    # Нажимаем на кнопку Мои питомцы
    driver.find_element_by_xpath('//a[contains(text(), "Мои питомцы")]').click()
    # Активируем ожидание пока не загрузится страница Мои питомцы:
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]')))

    # Установка Неявного ожидания на кнопку Выйти:
    driver.implicitly_wait(10)
    driver.find_element_by_xpath("//button[@onclick=\"document.location='/logout';\"]")

    # Находим всех питомцев
    driver.implicitly_wait(2)  # установка Неявного ожидания
    pets = driver.find_elements_by_xpath('//th[@scope="row"]')
    # Содержание статистики пользователя
    statistic_user = driver.find_element_by_xpath('//div[@class=".col-sm-4 left"]')
    # Находим всех без фото
    no_images = driver.find_elements_by_xpath('//img[@src=""]')
    # Находим все теги img
    img = driver.find_elements_by_css_selector('th[scope="row"] img')
    # Кол-во питомцев с фото
    have_images = (len(img) - len(no_images))
    # Находим локатор для извлечения Имени, Породы, Возраста
    pet_information = driver.find_elements_by_xpath('//text()/ancestor::td')
    # Локатор для имени
    driver.implicitly_wait(2)  # установка Неявного ожидания
    names = driver.find_elements_by_xpath('//*[@id="all_my_pets"]//td[1]')
    names_list = [x.text for x in names]  # Создаём список имён
    print('\nСписок Имён:', names_list)
    names_unique = list(set(names_list))  # поиск уникальных имён
    print('Уникальные Имена:', names_unique)
    # Локатор для профиля питомца:
    driver.implicitly_wait(2)  # установка Неявного ожидания
    pet_profile = driver.find_elements_by_xpath('//td/ancestor::tr')
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
    assert len(names_list) == len(names_unique)  # длина списка совпадает с кол-вом уникальных
    # 5.Проверяем, что в списке нет повторяющихся питомцев:
    assert len(pet_profile_list) == len(pet_profile_unique)  # длина списка совпадает с кол-вом уникальных
