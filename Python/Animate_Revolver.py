from tkinter import *
import threading
from PIL import Image, ImageTk
import simpleaudio as SAudio


# Анимация выстрела
def run_gif_animation_shot(image_path, sound_path):
    root = Tk()  # Создаём окно

    # Выводим окно поверх остальных:
    # root.lift()
    root.attributes('-topmost', True)

    # Делаем окно по центру
    w, h = 370, 300
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) / 2
    y = (sh - h) / 2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

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

    def play_sound(sound_path):
        wave_obj = SAudio.WaveObject.from_wave_file(sound_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    # Функция закрытия:
    def close_window():
        root.destroy()

    # Функция для обновления кадров анимации
    def update(uframe):
        label.configure(image=frames[uframe])
        uframe = (uframe + 1) % len(frames)
        # Воспроизведём звук на определенном кадре анимации:
        if uframe == 18:
            threading.Thread(target=play_sound, args=(sound_path,)).start()
        # Повтор анимации:
        root.after(100, update, uframe)
        # Закрываем окно после указанного кол-ва мсек:
        root.after(2500, close_window)

    root.after(100, update, 0)
    root.mainloop()


# Пример использования функции
# image_path = 'sounds/shot_revolver.gif'
# sound_path = 'sounds/shot.wav'
# run_gif_animation_shot(image_path, sound_path)


# Анимация спускового крючка
def run_gif_animation_empty(image_path, sound_path):
    root = Tk()  # Создаём окно

    # Выводим окно поверх остальных:
    # root.lift()
    root.attributes('-topmost', True)

    # Делаем окно по центру
    w, h = 370, 300
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) / 2
    y = (sh - h) / 2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

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

    def play_sound(sound_path):
        wave_obj = SAudio.WaveObject.from_wave_file(sound_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    # Функция закрытия:
    def close_window():
        root.destroy()

    # Функция для обновления кадров анимации
    def update(uframe):
        label.configure(image=frames[uframe])
        uframe = (uframe + 1) % len(frames)
        # Воспроизведём звук на определенном кадре анимации:
        if uframe == 16:
            threading.Thread(target=play_sound, args=(sound_path,)).start()
        # Повтор анимации:
        root.after(100, update, uframe)
        # Закрываем окно после указанного кол-ва мсек:
        root.after(1880, close_window)

    root.after(100, update, 0)
    root.mainloop()


# Пример использования функции
# image_path = 'sounds/misfire_empty.gif'
# sound_path = 'sounds/empty.wav'
# run_gif_animation_empty(image_path, sound_path)


# Анимация осечки
def run_gif_animation_misfire(image_path, sound_path):
    root = Tk()  # Создаём окно

    # Выводим окно поверх остальных:
    # root.lift()
    root.attributes('-topmost', True)

    # Делаем окно по центру
    w, h = 370, 300
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) / 2
    y = (sh - h) / 2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

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

    def play_sound(sound_path):
        wave_obj = SAudio.WaveObject.from_wave_file(sound_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    # Функция закрытия:
    def close_window():
        root.destroy()

    # Функция для обновления кадров анимации
    def update(uframe):
        label.configure(image=frames[uframe])
        uframe = (uframe + 1) % len(frames)
        # Воспроизведём звук на определенном кадре анимации:
        if uframe == 16:
            threading.Thread(target=play_sound, args=(sound_path,)).start()
        # Повтор анимации:
        root.after(100, update, uframe)
        # Закрываем окно после указанного кол-ва мсек:
        root.after(1880, close_window)

    root.after(100, update, 0)
    root.mainloop()


# Пример использования функции
# image_path = 'sounds/misfire_empty.gif'
# sound_path = 'sounds/misfire.wav'
# run_gif_animation_misfire(image_path, sound_path)


# Звуки для использования в Игре на двоих с осечкой
def gunshot_sounds(sound_path):
    wave_obj = SAudio.WaveObject.from_wave_file(sound_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()

# # Пример использования функции
# gunshot_sounds('sounds/shot.wav')
# gunshot_sounds('sounds/empty.wav')
# gunshot_sounds('sounds/misfire.wav')
