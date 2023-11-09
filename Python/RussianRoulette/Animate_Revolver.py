from tkinter import *
import threading
from PIL import Image, ImageTk
import simpleaudio as sa


def play_sound(sound_path):
    wave_obj = sa.WaveObject.from_wave_file(sound_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()


def screen_center(root):
    # Выводим окно поверх остальных:
    # root.lift()
    root.attributes('-topmost', True)

    # Делаем окно по центру
    w, h = 450, 330
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) / 2
    y = (sh - h) / 2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


# Анимация выстрела
def run_gif_animation_shot(image_path, sound_path):
    root = Tk()  # Создаём окно
    screen_center(root)

    # Загрузка gif-файла
    gif_image = Image.open(image_path)

    # Получение списка всех кадров анимации
    frames = []
    for frame in range(0, gif_image.n_frames):
        gif_image.seek(frame)
        frames.append(ImageTk.PhotoImage(gif_image))

    # Создание метки и установка первого кадра анимации
    label = Label(root)
    label.pack()
    label.configure(image=frames[0])

    # Функция для обновления кадров анимации
    def update_frames(uframe):
        label.configure(image=frames[uframe])
        uframe = (uframe + 1) % len(frames)
        # Воспроизведём звук на определенном кадре анимации:
        if uframe == 18:
            threading.Thread(target=play_sound, args=(sound_path,)).start()
        # Повтор анимации:
        root.after(100, update_frames, uframe)

    def close_window():
        for after_id in root.tk.eval('after info').split():
            root.after_cancel(after_id)
        root.destroy()

    # Запускаем цикл обновления кадров:
    root.after(100, update_frames, 0)
    # Установка длительности анимации и действие после:
    root.after(2500, close_window)
    # Установка обработчика закрытия окна
    root.protocol("WM_DELETE_WINDOW", close_window)

    root.mainloop()


# Пример использования функции
# image_path = 'sounds/shot_revolver.gif'
# sound_path = 'sounds/shot.wav'
# run_gif_animation_shot(image_path, sound_path)


# Анимация осечки или холостого спуска
def run_gif_animation_no_shot(image_path, sound_path):
    root = Tk()  # Создаём окно
    screen_center(root)

    # Загрузка gif-файла
    gif_image = Image.open(image_path)

    # Получение списка всех кадров анимации
    frames = []
    for frame in range(0, gif_image.n_frames):
        gif_image.seek(frame)
        frames.append(ImageTk.PhotoImage(gif_image))

    # Создание метки и установка первого кадра анимации
    label = Label(root)
    label.pack()
    label.configure(image=frames[0])

    # Функция для обновления кадров анимации
    def update_frames(uframe):
        label.configure(image=frames[uframe])
        uframe = (uframe + 1) % len(frames)
        # Воспроизведём звук на определенном кадре анимации:
        if uframe == 16:
            threading.Thread(target=play_sound, args=(sound_path,)).start()
        # Повтор анимации:
        root.after(100, update_frames, uframe)

    def close_window():
        for after_id in root.tk.eval('after info').split():
            root.after_cancel(after_id)
        root.destroy()

    # Запускаем цикл обновления кадров:
    root.after(100, update_frames, 0)
    # Установка длительности анимации и действие после:
    root.after(2000, close_window)
    # Установка обработчика закрытия окна
    root.protocol("WM_DELETE_WINDOW", close_window)

    root.mainloop()


# Пример использования функции
# image_path = 'sounds/misfire_empty.gif'
# sound_path = 'sounds/empty.wav'
# run_gif_animation_no_shot(image_path, sound_path)
