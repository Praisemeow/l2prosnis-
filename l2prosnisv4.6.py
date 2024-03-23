import time
import win32api
import win32gui
import win32con
import pyautogui
import keyboard
import sys
import os
import pyperclip
import telebot
import threading
import pywintypes
import json

# Загрузите конфигурацию из файла
with open("config.json", "r") as config_file:
    config_data = json.load(config_file)

# Используйте значения из config_data
coordinates = config_data["coordinates"]
enable_checks = config_data["enable_checks"]
s = config_data["s"]
rgb_change_thresholds = config_data["rgb_change_thresholds"]
target_colors = config_data["target_colors"]
token = config_data["token"]
chatid = config_data["chatid"]
pause_hotkey = config_data["pause_hotkey"]
exit_hotkey = config_data["exit_hotkey"]
toggle_hotkeys = config_data["toggle_hotkeys"]
copy_mouse_cords_hotkey = config_data["copy_mouse_cords_hotkey"]
target_class = config_data["target_class"]

# Присвойте значения переменным
x1, y1 = coordinates[0]["x"], coordinates[0]["y"]
x2, y2 = coordinates[1]["x"], coordinates[1]["y"]
x3, y3 = coordinates[2]["x"], coordinates[2]["y"]
x4, y4 = coordinates[3]["x"], coordinates[3]["y"]
x5, y5 = coordinates[4]["x"], coordinates[4]["y"]

enable_1_check = enable_checks[0]
enable_2_check = enable_checks[1]
enable_3_check = enable_checks[2]
enable_4_check = enable_checks[3]
enable_5_check = enable_checks[4]

RGB_CHANGE_THRESHOLD1 = rgb_change_thresholds[0]
RGB_CHANGE_THRESHOLD2 = rgb_change_thresholds[1]
RGB_CHANGE_THRESHOLD3 = rgb_change_thresholds[2]
RGB_CHANGE_THRESHOLD4 = rgb_change_thresholds[3]
RGB_CHANGE_THRESHOLD5 = rgb_change_thresholds[4]

TARGET_COLOR1 = tuple(target_colors[0])
TARGET_COLOR2 = tuple(target_colors[1])
TARGET_COLOR3 = tuple(target_colors[2])
TARGET_COLOR4 = tuple(target_colors[3])
TARGET_COLOR5 = tuple(target_colors[4])

TOKEN = token
chatid = chatid
pause_hotkey = pause_hotkey
exit_hotkey = exit_hotkey
toggle_1 = toggle_hotkeys[0]
toggle_2 = toggle_hotkeys[1]
toggle_3 = toggle_hotkeys[2]
toggle_4 = toggle_hotkeys[3]
toggle_5 = toggle_hotkeys[4]
copy_mouse_cords = copy_mouse_cords_hotkey
target_class = target_class


# Получение пути к директории, где находится текущий скрипт
script_directory = os.path.dirname(os.path.abspath(__file__))

# Получение пути к текущей рабочей директории (где был запущен скрипт)
current_working_directory = os.getcwd()

# Добавление обоих путей в sys.path
sys.path.append(script_directory)
sys.path.append(current_working_directory)

print("script_directory:", script_directory)
print("current_working_directory:", current_working_directory)
# Список всех импортированных модулей
imported_modules = list(sys.modules.keys())
print('-------------------------------------------------------')

# Вывести список модулей
for module_name in imported_modules:
    print(module_name)

print('-------------------------------------------------------')

print("enable_1_check =", enable_1_check)
print("enable_2_check =", enable_2_check)
print("enable_3_check =", enable_3_check)
print("enable_4_check =", enable_4_check)
print("enable_5_check =", enable_5_check)
print("Every seconds =", s)
print("pause_hotkey is =", pause_hotkey)
print("exit_hotkey is =", exit_hotkey)
print("toggle_1 is =", toggle_1)
print("toggle_2 is =", toggle_2)
print("toggle_3 is =", toggle_3)
print("toggle_4 is =", toggle_4)
print("toggle_5 is =", toggle_5)
print("copy_mouse_cords is =", copy_mouse_cords)

print('-------------------------------------------------------')

print('Скрипт запущен')



# Инициализируем бота
bot = telebot.TeleBot(TOKEN)

# Переменная для отслеживания статуса паузы
paused = False
exit_requested = False  # Переменная для отслеживания запроса на завершение скрипта

def get_windows_by_class(class_name):
    windows = []
    win32gui.EnumWindows(lambda hwnd, result: result.append(hwnd) if win32gui.GetClassName(hwnd) == class_name else None, windows)
    return windows


def check_pixel_color_in_all_windows(class_name):
    global paused, exit_requested

    while True:
        if not paused and not exit_requested:
            try:
                # Get all windows with the specified class
                windows = get_windows_by_class(class_name)

                for window_handle in windows:
                    # Get window coordinates
                    window_rect = win32gui.GetWindowRect(window_handle)

                    # Get device context for the window
                    device_context = win32gui.GetWindowDC(window_handle)

                    # Get pixel colors
                    pixel_colors = [
                        win32gui.GetPixel(device_context, x, y)
                        for x, y in [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5)]
                    ]

                    # Extract RGB components for each pixel
                    for i, pixel_color in enumerate(pixel_colors, start=1):
                        red, green, blue = pixel_color & 255, (pixel_color >> 8) & 255, (pixel_color >> 16) & 255

                        # Check and send message for each pixel
                        if i == 1 and enable_1_check and (
                                abs(red - TARGET_COLOR1[0]) >= RGB_CHANGE_THRESHOLD1 or
                                abs(green - TARGET_COLOR1[1]) >= RGB_CHANGE_THRESHOLD1 or
                                abs(blue - TARGET_COLOR1[2]) >= RGB_CHANGE_THRESHOLD1
                        ):
                            window_title = win32gui.GetWindowText(window_handle)
                            message = f"{window_title} #1 Pixel change: ({red}, {green}, {blue})"
                            bot.send_message(chat_id=chatid, text=message)

                        elif i == 2 and enable_2_check and (
                                abs(red - TARGET_COLOR2[0]) >= RGB_CHANGE_THRESHOLD2 or
                                abs(green - TARGET_COLOR2[1]) >= RGB_CHANGE_THRESHOLD2 or
                                abs(blue - TARGET_COLOR2[2]) >= RGB_CHANGE_THRESHOLD2
                        ):
                            window_title = win32gui.GetWindowText(window_handle)
                            message = f"{window_title} #2 Pixel change: ({red}, {green}, {blue})"
                            bot.send_message(chat_id=chatid, text=message)

                        elif i == 3 and enable_3_check and (
                                abs(red - TARGET_COLOR3[0]) >= RGB_CHANGE_THRESHOLD3 or
                                abs(green - TARGET_COLOR3[1]) >= RGB_CHANGE_THRESHOLD3 or
                                abs(blue - TARGET_COLOR3[2]) >= RGB_CHANGE_THRESHOLD3
                        ):
                            window_title = win32gui.GetWindowText(window_handle)
                            message = f"{window_title} #3 Pixel change: ({red}, {green}, {blue})"
                            bot.send_message(chat_id=chatid, text=message)

                        elif i == 4 and enable_4_check and (
                                abs(red - TARGET_COLOR4[0]) >= RGB_CHANGE_THRESHOLD4 or
                                abs(green - TARGET_COLOR4[1]) >= RGB_CHANGE_THRESHOLD4 or
                                abs(blue - TARGET_COLOR4[2]) >= RGB_CHANGE_THRESHOLD4
                        ):
                            window_title = win32gui.GetWindowText(window_handle)
                            message = f"{window_title} #4 Pixel change: ({red}, {green}, {blue})"
                            bot.send_message(chat_id=chatid, text=message)

                        elif i == 5 and enable_5_check and (
                                abs(red - TARGET_COLOR5[0]) <= RGB_CHANGE_THRESHOLD5 and
                                abs(green - TARGET_COLOR5[1]) <= RGB_CHANGE_THRESHOLD5 and
                                abs(blue - TARGET_COLOR5[2]) <= RGB_CHANGE_THRESHOLD5
                        ):
                            window_title = win32gui.GetWindowText(window_handle)
                            message = f"{window_title} #5 Pixel change: ({red}, {green}, {blue})"
                            bot.send_message(chat_id=chatid, text=message)
                            print("Message sent!")

                    # Release device context
                    win32gui.ReleaseDC(window_handle, device_context)

            except pywintypes.error:
                print("Could not get pixel value.")
            time.sleep(s)
        else:
            time.sleep(s)


bot = telebot.TeleBot(TOKEN)

# Запуск бота в отдельном потоке
bot_thread = threading.Thread(target=bot.polling)
bot_thread.start()

# Функция для завершения работы бота
@bot.message_handler(commands=['stop'])
def botscript_exit(message):
    bot.reply_to(message, 'Бот завершает работу.')
    bot.stop_polling()
    exit_script()

@bot.message_handler(commands=['pause'])
def botscript_pause(message):
    if paused:
        bot.reply_to(message, 'Скрипт возобновлен.')
    else:
        bot.reply_to(message, 'Скрипт приостановлен.')
    toggle_pause()




def copy_mouse_coordinates_and_pixel_color():
    # Получение координат мыши
    x, y = pyautogui.position()

    # Получение цвета пикселя
    pixel_color = pyautogui.pixel(x, y)

    # Форматирование данных
    data_to_copy = f"Mouse Coordinates: ({x}, {y})\nPixel Color: {pixel_color}"
    print(data_to_copy)
    # Помещение данных в буфер обмена
    pyperclip.copy(data_to_copy)


# Функция для паузы и возобновления скрипта
def toggle_pause():
    global paused
    paused = not paused
    if paused:
        print("Скрипт приостановлен.")
    else:
        print("Скрипт возобновлен.")

# Функция для завершения скрипта
def exit_script():
    global exit_requested
    exit_requested = True
    print("Скрипт завершен.")

def toggle_1_check():
    global enable_1_check
    enable_1_check = not enable_1_check
    print(f"Проверка 1 включена: {enable_1_check}")
def toggle_2_check():
    global enable_2_check
    enable_2_check = not enable_2_check
    print(f"Проверка 2 включена: {enable_2_check}")
def toggle_3_check():
    global enable_3_check
    enable_3_check = not enable_3_check
    print(f"Проверка 3 включена: {enable_3_check}")
def toggle_4_check():
    global enable_4_check
    enable_4_check = not enable_4_check
    print(f"Проверка 4 включена: {enable_4_check}")
def toggle_5_check():
    global enable_5_check
    enable_5_check = not enable_5_check
    print(f"Проверка 5 включена: {enable_5_check}")


# Определение хоткеев (например, Ctrl + H и Ctrl + C)
keyboard.add_hotkey(toggle_1, toggle_1_check)
keyboard.add_hotkey(toggle_2, toggle_2_check)
keyboard.add_hotkey(toggle_3, toggle_3_check)
keyboard.add_hotkey(toggle_4, toggle_4_check)
keyboard.add_hotkey(toggle_5, toggle_5_check)


keyboard.add_hotkey(copy_mouse_cords, copy_mouse_coordinates_and_pixel_color)

# Ожидание комбинации клавиш для паузы/возобновления скрипта
keyboard.add_hotkey(pause_hotkey, toggle_pause)
# Ожидание комбинации клавиш для завершения скрипта
keyboard.add_hotkey(exit_hotkey, exit_script)

# Запуск проверки в фоновом режиме
if __name__ == "__main__":
    check_pixel_color_in_all_windows(target_class)

