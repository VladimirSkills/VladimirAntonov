"""
<><>REDIS<><>
"""
import redis
import json

cache = redis.Redis(
    host= 'redis-12059.c52.us-east-1-4.ec2.cloud.redislabs.com',
    port=12059,
    password='rNftZEI9Wu6yP5WXl5vqykrk1dC3Jlku'
)

# ШАГ 1: Создание словаря
data = {
    'Владислав': '79083679393',
    'Сергей': '79272145115',
    'Данил': '79276149119',
    'Николай': '79376151441'
}  # создаём словарь для записи

# ШАГ 2: Запись в кэш и вывод
cache.set('data', json.dumps(data))  # записываем в кеш в строку
converted_data = json.loads(cache.get('data'))  # переводим данные из кэша обратно в словарь

listname = ', '.join(list(map(str, converted_data.keys()))) # делаем читабельный вид
print(f"Создан список контактов Ваших друзей: {listname}")
names = input(f'Введите имя друга для получения телефона: ')

# ШАГ 3: Удаление
print(f"Его телефон: +{converted_data.get(names)}")
delit = input(f'Удалить контакты? y/n ')
for i in delit:
    if i == "y":
        cache.delete('data')  # чистим кэш
        print(cache.get('data'))
    else:
        print(f"Контакты сохранены: \n{converted_data}")
