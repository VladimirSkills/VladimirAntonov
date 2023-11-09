from Animate_Revolver import run_gif_animation_shot, run_gif_animation_no_shot
from colorama import init
from colorama import Fore
import random
import time
init()


# python -m nuitka --follow-imports Compile_Single_misfire.py
def russian_roulette_misfire():
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
                if shooter_choice == 6:
                    print(Fore.LIGHTYELLOW_EX, "Вас спасёт только Осечка! :)", sep='')
                    time.sleep(2)
                print(Fore.RESET, "\nКрутим барабан...", sep='')
                time.sleep(1)
                print(Fore.LIGHTCYAN_EX, f"Стрелок спускает курок!", sep='')
                time.sleep(1)
                shot = random.choice(range(1, 7))

                if shot == bullet_chamber_numbers or shot in bullet_chamber_numbers and shot != misfire:
                    run_gif_animation_shot('sounds/shot_revolver.gif', 'sounds/shot.wav')
                    print(Fore.LIGHTRED_EX, f"Выстрел! [\u25cf] || Патронник № {shot}", sep='')
                elif shot == misfire and int(misfire) in bullet_chamber_numbers:
                    run_gif_animation_no_shot('sounds/misfire_empty.gif', 'sounds/misfire.wav')
                    print(Fore.LIGHTBLUE_EX, f"Осечка!!! [\u2665] || Патронник № {shot}", sep='')
                else:
                    run_gif_animation_no_shot('sounds/misfire_empty.gif', 'sounds/empty.wav')
                    print(Fore.LIGHTYELLOW_EX, f"Пустой! ~\u263B~ || Патронник № {shot}", sep='')
                print(Fore.YELLOW, f"\n@ https://t.me/amusing_python", sep='')
                print(input(f"{Fore.WHITE}[!] Для выхода нажмите Enter ->"), sep='')
                break
        except ValueError:
            print("Нужно ввести количество патронов от 1 до 6!")


def main():
    russian_roulette_misfire()


if __name__ == '__main__':
    main()
