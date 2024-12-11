import pyautogui
import keyboard

# Флаг для управления состоянием программы
running = True

def coords():
    """Функция для вывода текущих координат мыши."""
    x, y = pyautogui.position()
    print(f"Координаты: {x}, {y}")

def stop_program():
    """Функция для остановки программы."""
    global running
    running = False
    print("Программа завершена")

# Назначение горячих клавиш
keyboard.add_hotkey('2', lambda: coords())  # Вывод координат при нажатии клавиши '2'
keyboard.add_hotkey('esc', stop_program)    # Завершение программы при нажатии 'Esc'

# Цикл, удерживающий программу активной
while running:
    pass
