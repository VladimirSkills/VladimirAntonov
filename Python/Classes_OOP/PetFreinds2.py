from PetFreinds1 import Cat

# cat1 = Cat(name="Барон", gender="Мальчик", age=2)
# cat2 = Cat(name="Сэм", gender="Мужик", age=10)
cat1 = Cat('Барон', 'Мальчик', 2)
cat2 = Cat('Сэм', 'Мужик', 10)

print(f"Имя: {cat1.name}, Пол: {cat1.gender}, Возраст: {cat1.age}")
print(f"Имя: {cat2.name}, Пол: {cat2.gender}, Возраст: {cat2.age}")
print('')
print("Имя:", cat1.getName())
print("Пол:", cat1.getGender())
print("Возраст:", cat1.getAge())
print('')
print("getAll-1:", cat1.getAll())
print("getAll-2:", cat2.getAll())



