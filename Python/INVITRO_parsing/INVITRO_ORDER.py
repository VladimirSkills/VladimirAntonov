import json
import random
import requests
import time
from time import perf_counter
from bs4 import BeautifulSoup as BSp
from fake_useragent import UserAgent
UsAgent = UserAgent().random


headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'User-Agent': UsAgent
    }


def invitro_parsing():
    # Засекаем таймер выполнения кода:
    start = perf_counter()
    # Создаём сессию:
    ses = requests.Session()
    resp1 = ses.get('https://www.invitro.ru/analizes/for-doctors/samara/', headers=headers)
    soup1 = BSp(resp1.text, 'lxml')
    # Обозначим локатор для разделов главного меню:
    main_menu = soup1.select('a.sidebar_no_js.side-bar__link')
    title_list = []
    # Извлечём названия разделов и ссылки на них:
    for item in main_menu:
        menu_title = item.text
        if item['href']:
            menu_title_link = 'https://www.invitro.ru' + item['href']
        else:
            menu_title_link = 'https://www.invitro.ru' + item.next_sibling.find_all('li', class_="side-bar-second__items")[0].find('a')['href']
        # Ограничим сбор информации разделом "Анализы":
        if "Анализы" in menu_title:
            # Отправим запрос для получения HTML-кода страницы раздела "Анализы":
            resp2 = ses.get(url=menu_title_link, headers=headers)
            soup2 = BSp(resp2.text, 'lxml')
            analyzes_list = []
            # Обозначим локатор для всех подразделов раздела "Анализы":
            analyzes = soup2.find_all('div', class_="side-bar__block")[1].find_all('li', class_="side-bar-second__items")
            # Ограничим сбор информации первыми тремя подразделами:
            for sub in analyzes[:3]:
                # Для каждого подраздела получим Имя и Ссылку:
                analyzes_title = sub.find('a').text
                analyzes_title_link = 'https://www.invitro.ru' + sub.find('a')['href']
                sub_analyze_list = []
                # В каждом подразделе получим локатор на блок с анализами:
                if sub.find('ul', class_="side-bar-third__list"):
                    for subname in sub.find('ul', class_="side-bar-third__list"):
                        # Получим названия блоков с анализами и ссылку на них:
                        title_name = subname.text
                        title_name_link = 'https://www.invitro.ru' + subname.find('a')['href']
                        # Отправим запрос по каждой ссылке блока с анализами для получения страниц с анализами:
                        resp3 = ses.get(url=title_name_link, headers=headers)
                        soup3 = BSp(resp3.text, 'lxml')

                        subsection_list = []
                        # Обозначим локатор на все анализы на странице:
                        block = soup3.find('div', class_="pagination-items").find_all('div', class_="analyzes-list")
                        for items in block:
                            if items.find('div', class_="analyzes-item__title"):
                                # Получим имя и ссылку на анализ:
                                name = items.find('div', class_="analyzes-item__title").text.strip()
                                link = 'https://www.invitro.ru' + items.find('div', class_="analyzes-item__title").find('a')['href']
                            else:
                                continue
                            # Вывод на печать всех ссылок на анализы - в случае ошибки поможет понять,
                            # после прохода какого анализа возникла ошибка
                            # (т.е. она может быть на этом анализе или на следующем):
                            print(link)
                            # Получим условия акции, если она есть:
                            promotion = items.find('div', class_="ri-promotion-items__scroller")
                            if promotion.find('a'):
                                promotion_link = 'https://www.invitro.ru' + promotion.find_all('a')[0]['href']
                            else:
                                promotion_link = 'Без акции'
                            # Получим описание анализа:
                            description = items.find('div', class_="analyzes-item__description").text.replace('\n', '').strip()
                            # Отправляем запрос по ссылке для каждого анализа для получения дополнительной информации:
                            resp4 = ses.get(url=link, headers=headers)
                            soup4 = BSp(resp4.text, 'lxml')
                            # Артикул анализа:
                            articul = soup4.find('div', class_="info-block__section--article").find('span', class_="info-block__price").text.strip()
                            # Стоимость анализа:
                            price = soup4.find('div', class_="info-block__section--price").find('span', class_="info-block__price").text.replace(' руб', '').strip()
                            # Время готовности результата:
                            ready_time = soup4.find('div', class_="info-block__section--date").find('span', class_="radio__text").find('span').previous_sibling.text.strip()
                            # Пример с результатами в файле PDF:
                            if soup4.find('div', class_="test_result_example"):
                                download_example = 'https://www.invitro.ru' + soup4.find('div', class_="test_result_example") \
                                                       .find('a', class_="direct-item__name")['href']
                            else:
                                download_example = 'Нет примера'
                            # Условия подготовки перед анализом:
                            preparation = soup4.select('div.article')[1].text.replace('\n', '').replace(' ', ' ').strip()
                            if soup4.select('div.article')[3]:
                                # Показания к назначению:
                                testimony = soup4.select('div.article')[2].text.replace('\n', '').strip()
                                # Интерпретация результатов:
                                results = soup4.select('div.article')[3].text.replace('\n\n', '').replace(' ', ' ').strip()
                            else:
                                continue

                            # Создаём вложенные друг в друга списки в виде словарей от частного к общему:
                            subsection_list.append({
                                'Наименование': name,
                                'Ссылка': link,
                                'Артикул': articul,
                                'Цена': price,
                                'Акция': promotion_link,
                                'Описание': description.replace('   ', ''),
                                'Готовность': ready_time,
                                'Пример': download_example,
                                'Подготовка': preparation,
                                'Показания': testimony,
                                'Результаты': results
                            })

                            time.sleep(random.randrange(1, 3))

                        sub_analyze_list.append({
                            'Анализ': title_name,
                            'Ссылка': title_name_link,
                            'Содержание': subsection_list
                        })
                else:
                    sub_analyze_list = "Нет подразделов!"

                analyzes_list.append({
                    'Группа': analyzes_title,
                    'Ссылка': analyzes_title_link,
                    'Исследования': sub_analyze_list
                })

            title_list.append({
                'Раздел Меню': menu_title,
                'Ссылка': menu_title_link,
                'Подраздел': analyzes_list
            })

        else:
            analyzes_list = 'Парсинг данного подраздела не осуществляется!'
            title_list.append({
                'Раздел Меню': menu_title,
                'Ссылка': menu_title_link,
                'Подраздел': analyzes_list
            })
        # Сохраняем данные в формат json:
        with open("data_invitro/Menu_Biochim_Analyzes_1.json", 'w', encoding='utf-8') as file:
            json.dump(title_list, file, indent=4, ensure_ascii=False)

    # Фиксируем время выполнения:
    print(f"\nTime: {(perf_counter() - start)/60:.02f} мин.")


def get_promotions():
    url_discount = 'https://www.invitro.ru/samara/ak/'
    ses = requests.Session()
    resp = ses.get(url_discount, headers=headers)
    soup = BSp(resp.text, 'lxml')
    promotions_list = []
    promotions_block = soup.find('div', class_="actions__items").find_all('div', class_="actions__item")
    count = 1
    for item in promotions_block:
        title = item.find('img')['title'].strip()
        href = 'https://www.invitro.ru' + item.find('a')['href']
        ready_time = item.find('div', class_="actions__date-finish").text
        response = ses.get(href, headers=headers)
        soup2 = BSp(response.text, 'lxml')

        if soup2.find('h2', class_="banner-menu__title t_36 blue_flat_2"):
            name = soup2.find('h2', class_="banner-menu__title t_36 blue_flat_2").text.strip()
            description = soup2.find('div', class_="banner-menu__text t_16").text.replace('\n\n', '\n').strip()
        elif len(soup2.find('div', id="titlePage").find('h1').text) > 5:
            name = soup2.find('div', id="titlePage").text.strip()
            description = soup2.find('div', class_="article article--p0").text.strip().split('\n')[0]
        elif soup2.find('h1', class_="dark"):
            name = soup2.find('h1', class_="dark").text
            description = soup2.find('p', class_="main_banner_desc dark").text
        else:
            name = None
            description = None
        if soup2.find('a', class_="price-block__terms-link popup-pdf t_16"):
            conditions_link = 'https://www.invitro.ru' + soup2.find('a', class_="price-block__terms-link popup-pdf t_16")['href']
        else:
            conditions_link = None
        if soup2.find('div', class_="price-block__value-container"):
            name_cost = 'Стоимость'
            price = soup2.find('div', class_="price-block__value-container").text.replace(' ₽', '').strip()
        else:
            name_cost = 'Стоимость'
            price = None

        promotions_list.append({
            'Акция': title,
            'Ссылка': href,
            'Действие': ready_time,
            'Заголовок': name,
            'Описание': description,
            'Условия акции': conditions_link,
            f"{name_cost}": price,
        })
        time.sleep(random.randrange(1, 3))
        print(f"[+] The page at link {count} has been recorded!")
        count += 1

    with open("data_invitro/Actions.json", 'w', encoding='utf-8') as file:
        json.dump(promotions_list, file, indent=4, ensure_ascii=False)


def main():
    invitro_parsing()
    # get_promotions()


if __name__ == '__main__':
    main()
