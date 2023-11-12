import simpleaudio as sa
from colorama import init
from colorama import Fore
import random
import time
init()


def gunshot_sounds(sound_path):
    wave_obj = sa.WaveObject.from_wave_file(sound_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()


# pyinstaller -i D:\Папа\SkillFactory\hat_magic.ico Compile_Pair_misfire.py -F
def russian_roulette_pair_misfire():
    """Nuitka — компилятор Python. Установка: pip install Nuitka
    Команда для компиляции в файл.exe: python -m nuitka --follow-imports Compile_Pair_misfire.py"""
    first_shooter = input(f"{Fore.LIGHTCYAN_EX}Введите Nickname ПЕРВОГО стрелка: ")
    second_shooter = input(f"{Fore.LIGHTBLUE_EX}Введите Nickname ВТОРОГО стрелка: ")
    while True:
        try:
            shooter_choice = int(input(f"{Fore.LIGHTWHITE_EX}Выберите число патронов от 1 до 6: "))

            if 1 <= shooter_choice <= 6:
                bullet_chamber_numbers = random.sample(range(1, 7), shooter_choice)
                chambers = ', '.join(map(str, sorted(bullet_chamber_numbers)))

                if shooter_choice == 1:
                    misfire = random.choice(range(1, 7))
                else:
                    misfire = random.choice(bullet_chamber_numbers)
                print(Fore.LIGHTGREEN_EX, f"Патроны вложены в патронники №: {chambers}", sep='')
                time.sleep(2)
                if shooter_choice == 6:
                    print(Fore.LIGHTYELLOW_EX, "Господа, Вас спасёт только Осечка! :)", sep='')
                    time.sleep(2)

                count = 1
                bullet = 0
                while True:
                    print(Fore.RESET, "\nКрутим барабан... ", sep='')
                    if count % 2 != 0:
                        print(Fore.LIGHTCYAN_EX, f"Стрелок '{first_shooter.upper()}' спускает курок! ╦═━^━", sep='')
                        time.sleep(1)
                    else:
                        print(Fore.LIGHTBLUE_EX, f"Стрелок '{second_shooter.upper()}' спускает курок! ╦═━^━", sep='')
                        time.sleep(1)
                    shot = random.choice(range(1, 7))
                    if shot in bullet_chamber_numbers and shot != misfire + bullet:
                        print(Fore.LIGHTRED_EX, f"Выстрел! [\u25cf] || Патронник № {shot}", sep='')
                        gunshot_sounds('sounds/shot.wav')
                        time.sleep(0.5)
                        break
                    elif shot == misfire and int(misfire) + bullet in bullet_chamber_numbers:
                        print(Fore.LIGHTMAGENTA_EX, f"Осечка!!! [\u2665] || Патронник № {shot}", sep='')
                        gunshot_sounds('sounds/misfire.wav')
                        time.sleep(0.5)
                        bullet += 6
                    else:
                        print(Fore.LIGHTYELLOW_EX, f"Пустой! ~\u263B~ || Патронник № {shot}", sep='')
                        gunshot_sounds('sounds/empty.wav')
                        time.sleep(0.5)
                    count += 1
                print(Fore.LIGHTWHITE_EX, f"\n<╦═━^━ Конец игры на {count} выстреле!\n", sep='')
                print(Fore.YELLOW, f"@ https://t.me/amusing_python", sep='')
                # print(input(f"{Fore.WHITE}[!] Для выхода нажмите Enter ->"), sep='')
                break
        except ValueError:
            print(Fore.LIGHTYELLOW_EX, "[INFO] Нужно ввести количество патронов от 1 до 6!", sep='')


russian_roulette_pair_misfire()
