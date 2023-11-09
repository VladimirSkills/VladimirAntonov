"""
ИГРА РУССКАЯ РУЛЕТКА / Russian Roulette GAME
В револьвере 6 патронов. Стрелок должен вложить в барабан револьвера от 1 до 6 патронов и нажать на спусковой крючок.
Каждому отверстию патронника соответствует номер от 1 до 6. Патронникам с вложенными стрелком патронами, случайным
образом будут присвоены номера. Затем среди шести чисел, соответствующих номерам патронников, будет случайным образом
выбрано одно для выстрела. Если оно совпадёт с патронником, где вложен патрон, то появится надпись: "Выстрел",
если нет, тогда надпись: "Пустой!". Для более жизненной картины, в некоторых вариантах игры также будет иметь место
одна Осечка! Варианты игры "Русская рулетка":
-> Классика без осечек
-> Игра для одного с осечкой
-> Игра на двоих с осечкой

In a revolver, there are 6 cartridges. The shooter must load the revolver's chamber with 1 to 6 cartridges and pull the trigger.
Each chamber hole has a number from 1 to 6. The chambers with the loaded cartridges are randomly assigned numbers.
Then, one number among the six numbers corresponding to the chamber numbers is randomly chosen for the shot.
If it matches the chamber with the loaded cartridge, the message "Shot" will appear. If not, the message "Empty!".
For a more realistic scenario, in some game variations, there will also be one Misfire!
The game variations of "Russian roulette" are:
- Classic version without misfires
- Single player game with a misfire
- Two-player game with a misfire
"""

from Animate_Revolver import run_gif_animation_shot, run_gif_animation_no_shot, play_sound
import random
import time


"""
РУССКАЯ РУЛЕТКА. Классика без осечек с анимацией.
Classic version without misfires with animation.
"""


def russian_roulette_classic():
    """В револьвере роль патронника играют отверстия его барабана, также называемые кáморами."""
    while True:
        try:
            # Ввод количества патронов, помещаемых в барабан револьвера:
            # C ростом количества патронов в барабане, вероятность выстрела повышается!
            shooter_choice = int(input("Выберите число патронов от 1 до 6: "))
            if 1 <= shooter_choice <= 6:
                # Генерация случайных номеров, соответствующих отверстиям патронника (каморы).
                # Присваиваем каждому патрону, вложенному в камору - свой номер в патроннике:
                bullet_chamber_numbers = random.sample(range(1, 7), shooter_choice)
                chambers = ', '.join(map(str, sorted(bullet_chamber_numbers)))
                print(f"Патроны вложены в патронники №: {chambers}")

                # Задаём случайный выбор номера патронника в барабане для выстрела:
                shot = random.choice(range(1, 7))
                # Крутим барабан:
                print("\nКрутим барабан...")
                time.sleep(1)
                print(f"Стрелок спускает курок!")
                time.sleep(1)

                # Сравниваем, что номер патронника для выстрела совпадает с номером, где находится патрон:
                if shot == bullet_chamber_numbers or shot in bullet_chamber_numbers:
                    # Запустим анимацию, зареалим выстрел и пошумим:
                    run_gif_animation_shot('sounds/shot_revolver.gif', 'sounds/shot.wav')
                    print(f"\u27A4 Выстрел! 💥 || Патронник № {shot}")
                else:
                    run_gif_animation_no_shot('sounds/misfire_empty.gif', 'sounds/empty.wav')
                    print(f"Пустой! \u263B || Патронник № {shot}")
                break
        except ValueError:
            print("Нужно ввести количество патронов от 1 до 6!")


# Запуск игры
def main():
    russian_roulette_classic()


if __name__ == '__main__':
    main()


"""
РУССКАЯ РУЛЕТКА. Игра для одного с осечкой. Есть анимация.
Single player game with a misfire with animation.
"""


def russian_roulette_misfire():
    """В револьвере роль патронника играют отверстия его барабана, также называемые кáморами."""
    while True:
        try:
            # Ввод количества патронов, помещаемых в барабан револьвера:
            shooter_choice = int(input("Выберите число патронов от 1 до 6: "))
            if 1 <= shooter_choice <= 6:
                # Генерация случайных номеров, соответствующих отверстиям патронника (каморы).
                # Присваиваем каждому патрону, вложенному в камору - свой номер в патроннике:
                bullet_chamber_numbers = random.sample(range(1, 7), shooter_choice)
                chambers = ', '.join(map(str, sorted(bullet_chamber_numbers)))

                # Допустим, что фортуна ингода благоволит стрелкам и один раз возможна осечка при выстреле...
                # Тогда выберем случайным образом номер каморы с патроном, где будет осечка:
                if shooter_choice == 1:
                    misfire = random.choice(range(1, 7))
                else:
                    misfire = random.choice(bullet_chamber_numbers)
                print(f"Патроны вложены в патронники №: {chambers}")
                # Для любителей экстрима, вставляющих сразу все патроны в револьвер:
                if shooter_choice == 6:
                    print("Вас спасёт только Осечка!")
                    time.sleep(2)

                # Крутим барабан:
                print("\nКрутим барабан...")
                time.sleep(1)
                print(f"Стрелок спускает курок!")
                time.sleep(1)
                # Задаём случайный выбор номера патронника в барабане для выстрела:
                shot = random.choice(range(1, 7))

                # Сравниваем, что номер патронника для выстрела совпадает с номером, где находится патрон:
                if shot == bullet_chamber_numbers or shot in bullet_chamber_numbers and shot != misfire:
                    # Запустим анимацию, зареалим выстрел и пошумим:
                    run_gif_animation_shot('sounds/shot_revolver.gif', 'sounds/shot.wav')
                    print(f"\u27A4 Выстрел! 💥 || Патронник № {shot}")
                elif shot == misfire and int(misfire) in bullet_chamber_numbers:
                    run_gif_animation_no_shot('sounds/misfire_empty.gif', 'sounds/misfire.wav')
                    print(f"Осечка! \u2764 || Патронник № {shot}")
                else:
                    run_gif_animation_no_shot('sounds/misfire_empty.gif', 'sounds/empty.wav')
                    print(f"Пустой! ~\u263B~ || Патронник № {shot}")
                break
        except ValueError:
            print("Нужно ввести количество патронов от 1 до 6!")


# Запуск игры
def main():
    russian_roulette_misfire()


if __name__ == '__main__':
    main()


"""
РУССКАЯ РУЛЕТКА. Игра на двоих с осечкой. Без анимации
Two-player game with a misfire. No animation.
"""


def russian_roulette_pair_misfire():
    """В револьвере роль патронника играют отверстия его барабана, также называемые кáморами."""
    while True:
        try:
            # Ввод количества патронов, помещаемых в барабан револьвера:
            shooter_choice = int(input("Выберите число патронов от 1 до 6: "))
            if 1 <= shooter_choice <= 6:
                # Генерация случайных номеров, соответствующих отверстиям патронника (каморы).
                # Присваиваем каждому патрону, вложенному в камору - свой номер в патроннике:
                bullet_chamber_numbers = random.sample(range(1, 7), shooter_choice)
                chambers = ', '.join(map(str, sorted(bullet_chamber_numbers)))

                # Допустим, что фортуна ингода благоволит стрелкам и один раз возможна осечка при выстреле...
                # Тогда выберем случайным образом номер каморы с патроном, где будет осечка:
                if shooter_choice == 1:
                    misfire = random.choice(range(1, 7))
                else:
                    misfire = random.choice(bullet_chamber_numbers)
                print(f"Патроны вложены в патронники №: {chambers}")
                # Для любителей экстрима, вставляющих сразу все патроны в револьвер:
                if shooter_choice == 6:
                    print("Господа, Вас спасёт только Осечка!")
                    time.sleep(2)

                count = 1  # счёт кол-ва выстрелов
                bullet = 0  # отсечка для отмены осечек
                while True:
                    # Крутим барабан:
                    print("\nКрутим барабан...")
                    time.sleep(1)
                    if count % 2 != 0:  # Если нечётный, то первый.
                        print(f"Стрелок 1 спускает курок!")
                    else:
                        print(f"Стрелок 2 спускает курок!")
                    # Задаём случайный выбор номера патронника в барабане для выстрела:
                    shot = random.choice(range(1, 7))
                    # Сравниваем, что номер патронника для выстрела совпадает с номером, где находится патрон:
                    if shot in bullet_chamber_numbers and shot != misfire + bullet:
                        print(f"\u27A4 Выстрел! 💥 || Патронник № {shot}")
                        # Зареалим выстрел и пошумим...))
                        time.sleep(0.5)
                        play_sound('sounds/shot.wav')
                        break
                    elif shot == misfire and int(misfire) + bullet in bullet_chamber_numbers:
                        print(f"Осечка! \u2764 || Патронник № {shot}")
                        time.sleep(0.5)
                        play_sound('sounds/misfire.wav')
                        # После разового срабатывания осечки, делаем номер патронника с осечкой невалидным:
                        bullet += 6
                    else:
                        print(f"Пустой! ~\u263B~ || Патронник № {shot}")
                        time.sleep(0.5)
                        play_sound('sounds/empty.wav')
                    count += 1
                print(f"\n->\u2573<- Конец игры \u2620 на {count} выстреле!")
                break
        except ValueError:
            print("Нужно ввести количество патронов от 1 до 6!")


# Запуск игры
def main():
    russian_roulette_pair_misfire()


if __name__ == '__main__':
    main()
