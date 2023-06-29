import json
import random
from time import perf_counter
from bs4 import BeautifulSoup as BSp
import platform
import aiohttp
import aiofiles
import asyncio
from aiocsv import AsyncWriter
from fake_useragent import UserAgent
UsAgent = UserAgent().random


headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'User-Agent': UsAgent
    }


async def invitro_parsing_asyncio():
    # Засекаем таймер выполнения кода:
    start = perf_counter()
    # Создаём сессию:
    async with aiohttp.ClientSession() as ses:
        resp1 = await ses.get('https://www.invitro.ru/analizes/for-doctors/samara/', headers=headers)
        rest1 = await resp1.text()
        soup1 = BSp(rest1, 'lxml')
        # Обозначим локатор для разделов главного меню:
        main_menu = soup1.select('a.sidebar_no_js.side-bar__link')
        title_csv = [
            ['Раздел Меню', 'Ссылка', 'Группа', 'Ссылка', 'Анализ', 'Ссылка',
             'Наименование', 'Ссылка', 'Артикул', 'Цена', 'Акция', 'Описание', 'Готовность', 'Пример',
             'Подготовка', 'Показания', 'Результаты']
        ]
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
                resp2 = await ses.get(url=menu_title_link, headers=headers)
                rest2 = await resp2.text()
                soup2 = BSp(rest2, 'lxml')
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
                            resp3 = await ses.get(url=title_name_link, headers=headers)
                            rest3 = await resp3.text()
                            soup3 = BSp(rest3, 'lxml')

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
                                description = items.find('div', class_="analyzes-item__description").text.replace('\n', '').replace('   ', '').strip()
                                # Отправляем запрос по ссылке для каждого анализа для получения дополнительной информации:
                                resp4 = await ses.get(url=link, headers=headers)
                                rest4 = await resp4.text()
                                soup4 = BSp(rest4, 'lxml')
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
                                    'Описание': description,
                                    'Готовность': ready_time,
                                    'Пример': download_example,
                                    'Подготовка': preparation,
                                    'Показания': testimony,
                                    'Результаты': results
                                })
                                data_csv = [menu_title, menu_title_link, analyzes_title, analyzes_title_link,
                                            title_name, title_name_link, name, link, articul, price, promotion_link,
                                            description, ready_time, download_example, preparation, testimony, results]
                                title_csv.append(data_csv)

                                await asyncio.sleep(random.randrange(1, 3))

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
        async with aiofiles.open("data_invitro/Menu_Biochim_Analyzes_1.json", 'w', encoding='utf-8') as file:
            await file.write(json.dumps(title_list, indent=4, ensure_ascii=False))
        # Сохраняем данные в формат csv:
        async with aiofiles.open("data_invitro/Menu_Biochim_Analyzes_1.csv", 'w', newline='') as file:
            writer = AsyncWriter(file, delimiter=";")
            await writer.writerows(title_csv)

        # Фиксируем время выполнения:
        print(f"\nTime: {(perf_counter() - start)/60:.02f} мин.")
# Time: 7.27 мин. order
# Time: 4.95 мин. asyncio


async def main():
    await invitro_parsing_asyncio()


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
