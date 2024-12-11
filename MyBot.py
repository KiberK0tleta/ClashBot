import pyautogui
import matplotlib.pyplot as plt
from PIL import Image
import keyboard
import numpy as np
import time
import random
import cv2
import threading
import math
import mouse


def get_pixel_color(x, y):
    screenshot = pyautogui.screenshot() # Сделать скриншот всего экрана
    image = Image.frombytes('RGB', screenshot.size, screenshot.tobytes()) # Преобразовать скриншот в объект изображения
    
    r, g, b = image.getpixel((x, y))# Получить цвет пикселя
    return r, g, b




# screenshot = pyautogui.screenshot() # Сделать скриншот всего экрана
# screenshot.save("Skrin.png")
import mss
import numpy as np
import cv2



def find_piece(screenshot, rocket_template, accuracy, Import=True):
    if Import:
        screenshot_np = cv2.imread(screenshot, cv2.IMREAD_COLOR)
        if screenshot_np is None:
            print(f"Ошибка: не удалось загрузить изображение {screenshot}")
            return []
    else:
        screenshot_np = np.array(screenshot)
    
    rocket = cv2.imread(rocket_template, cv2.IMREAD_COLOR)
    if rocket is None:
        print(f"Ошибка: не удалось загрузить изображение {rocket_template}")
        return []
    
    result = cv2.matchTemplate(screenshot_np, rocket, cv2.TM_CCOEFF_NORMED)
    
    threshold = accuracy
    loc = np.where(result >= threshold)
    rocket_coordinates = []
    
    w, h = rocket.shape[1], rocket.shape[0]  # ширина и высота шаблона
    
    for pt in zip(*loc[::-1]):
        center_x = pt[0] + w // 2
        center_y = pt[1] + h // 2
        rocket_coordinates.append([center_x, center_y])
        # print(rocket_template, [center_x, center_y])
    
    return rocket_coordinates

def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def remove_close_duplicates(points, min_distance):
    result = []
    for point in points:
        is_close = False
        for existing_point in result:
            if distance(point, existing_point) < min_distance:
                is_close = True
                break
        if not is_close:
            result.append(point)
    return result

def find_and_click(image):
    stop = 0
    Find_Place = None
    while stop <= 3:
        screenshot = pyautogui.screenshot() # Сделать скриншот всего экрана
        screenshot.save("Skrin.png")        
        Place = find_piece("Skrin.png", image, 0.8, True)
        if Place:
            Find_Place = remove_close_duplicates(Place, 1)[0] 
            break
        print("Не нашел картинку")
        stop+=1
        # time.sleep(random_sec(0.1, 0.3))
    time.sleep(0.2)
    if not Find_Place:
        print("Не удалось найти картинку после 7 попыток.")
        return
    
    # Преобразуем координаты в целые числа
    x, y = int(Find_Place[0]), int(Find_Place[1])
    move_and_click(x, y)

def find_Zone_and_click(images):
    stop = 0
    Find_Place = None
    while stop <= 3:
        screenshot = pyautogui.screenshot()  # Сделать скриншот всего экрана
        screenshot.save("Skrin.png")
        for image in images:
            Place = find_piece("Skrin.png", image, 0.8, True)
            if Place:
                Find_Place = remove_close_duplicates(Place, 1)[0]
                break  # Выходим из цикла, если нашли совпадение
        if Find_Place:
            break  # Выходим из основного цикла, если нашли совпадение
        print("Не нашел картинку")
        stop += 1
        # time.sleep(random_sec(0.1, 0.3))
    time.sleep(0.2)
    if not Find_Place:
        print("Не удалось найти картинку после 3 попыток.")
        return

    # Преобразуем координаты в целые числа
    x, y = int(Find_Place[0]), int(Find_Place[1])
    move_and_click(x, y)


def LMB(x, y, exactly = 0):
    if(exactly == 0):
        pyautogui.moveTo(x+random.uniform(-10, 10), y+random.uniform(-10, 10))
        pyautogui.click(button='left')
    else:
        pyautogui.moveTo(x+random.uniform(-2, 2), y+random.uniform(-2, 2))
        pyautogui.click(button='left')

def move_and_click(x, y):
    pyautogui.moveTo(x, y)  # Переместить курсор
    time.sleep(0.3)  # Небольшая задержка
    pyautogui.click()  # Нажать левой кнопкой мыши


# Эта функция выводит текст в консоль с указанным цветом.
def print_colored(text, color_code):
    print(f'\033[{color_code}m{text}\033[0m')

# Стандартные цветовые коды:
# 31 — Красный
# 32 — Зеленый
# 33 — Желтый
# 34 — Синий
# 35 — Фиолетовый
# 36 — Голубой
from pynput.mouse import Button, Controller

mouse = Controller()

# Прокрутка вверх
mouse.scroll(0, 1)

# Прокрутка вниз
mouse.scroll(0, -1)


def to_left_bottom():
    pyautogui.moveTo(random.uniform(500, 800), random.uniform(200, 400))
    pyautogui.dragRel(random.uniform(400, 500), random.uniform(-300, -400), button='left', duration=random.uniform(0.1, 0.3))

def ship():
    to_left_bottom()
    time.sleep(1)
    LMB(620, 702)

def map():
    LMB(1298, 795)

def reset_zoom():
    print('Зум уменьшили')
    time.sleep(0.3)
    mouse.position = (847, 524)  # Перемещение мыши

    # Имитация нажатия клавиши Ctrl и прокрутки
    pyautogui.keyDown('ctrl')
    mouse.scroll(0, -10)  # Прокрутка вверх
    time.sleep(1)
    mouse.scroll(0, -10)  # Прокрутка вверх
    pyautogui.keyUp('ctrl')

    time.sleep(1)
    
    pyautogui.keyDown('ctrl')
    mouse.scroll(0, 1) 
    pyautogui.keyUp('ctrl')
    time.sleep(1)

mouse = Controller()
def drag_mouse(x_start, y_start, x_end, y_end, duration=1):
    # Перемещение к начальной точке
    mouse.position = (x_start, y_start)
    time.sleep(0.2)

    # Зажимаем левую кнопку мыши
    mouse.press(Button.left)

    # Разбиваем перемещение на маленькие шаги для плавности
    steps = 50
    dx = (x_end - x_start) / steps
    dy = (y_end - y_start) / steps
    for i in range(steps):
        mouse.position = (x_start + dx * i, y_start + dy * i)
        time.sleep(duration / steps)

    # Отпускаем левую кнопку мыши
    mouse.release(Button.left)

class Region:
    def __init__(self, x, y, name, army, zones, is_closed = False):
        self.x = x
        self.y = y
        self.name = name
        self.is_closed = is_closed
        self.army = army
        self.zones = zones

capital_peak        = Region(000,   000,  'Столичный_Пик',       'hogs',     ['green',          'rocket', 'gun'])
barbarian_camp      = Region(1053, 336,  'Лагерь_Варваров',     'hogs',     ['green', 'water', 'rocket', 'gun'])
wizard_valley       = Region(842, 431,  'Долина_Колдунов',     'hogs',     ['green', 'water',           'gun'])
baloon_lagoon       = Region(662, 597,  'Лагуна_Шаров',        'hogs',     ['green', 'water', 'rocket']       )
builders_workshop   = Region(982, 634,  'Мастерская_Строителя','hogs',     ['green', 'water',           'gun'])
dragon_cliffs       = Region(1208, 549,  'Драконьи_Утесы',      'hogs',  ['green', 'water']                 )
golem_quarry        = Region(470, 741,  'Карьер_Големов',      'hogs',     ['green', 'water', 'rocket']       )
skeleton_park       = Region(788, 796,  'Парк_Скелетов',       'hogs',     ['green', 'water', 'rocket', 'gun'])
goblin_shachts      = Region(1137, 790,  'Гоблинские_Шахты',    'hogs',     ['green', 'water', 'rocket', 'gun'])

is_esc = False

def esc():
    keyboard.wait('3')
    global is_esc
    is_esc = True

def reset_map():
    pyautogui.moveTo(1028+random.uniform(-50, 50), 346+random.uniform(-50, 50))
    pyautogui.dragRel(random.uniform(-15, 15), 180+random.uniform(-20, 10), button='left', duration=0.3+random.uniform(-0.1, 0.1))
    time.sleep(1)
    pyautogui.moveTo(1272, 575)
    pyautogui.dragRel(0, -135, button='left', duration=1)
    
    
    # drag_mouse(478, 700, 508, 504, duration=1)

def check_region(r, g, b):
    if(is_esc == True):
        return
    
    if (r > 230 and g > 230 and b > 230):
        return True
    
    return False

def check_map_raid():
    time.sleep(0.3)
    reset_map()
    time.sleep(0.3)
    screenshot = pyautogui.screenshot()
    image = screenshot.convert("RGB")

    # pyautogui.moveTo(capital_peak.x, capital_peak.y)
    # time.sleep(0.3)
    # r, g, b = image.getpixel((capital_peak.x, capital_peak.y))
    # capital_peak.is_closed = check_region(r, g, b)
    # if capital_peak.is_closed:
    #     print_colored('Пик закрыли', '32')
    # else:
    #     print_colored('Пик НЕ закрыли', '31')

    pyautogui.moveTo(barbarian_camp.x, barbarian_camp.y)
    time.sleep(0.3)
    r, g, b = image.getpixel((barbarian_camp.x, barbarian_camp.y))
    barbarian_camp.is_closed = check_region(r, g, b)
    if barbarian_camp.is_closed:
        print_colored('Варваров закрыли', '32')
    else:
        print_colored('Варваров НЕ закрыли', '31')

    pyautogui.moveTo(wizard_valley.x, wizard_valley.y)
    time.sleep(0.3)
    r, g, b = image.getpixel((wizard_valley.x, wizard_valley.y))
    wizard_valley.is_closed = check_region(r, g, b)
    if wizard_valley.is_closed:
        print_colored('Магов закрыли', '32')
    else:
        print_colored('Магов НЕ закрыли', '31')
    
    pyautogui.moveTo(baloon_lagoon.x, baloon_lagoon.y)
    time.sleep(0.3)
    r, g, b = image.getpixel((baloon_lagoon.x, baloon_lagoon.y))
    baloon_lagoon.is_closed = check_region(r, g, b)
    if baloon_lagoon.is_closed:
        print_colored('Шары закрыли', '32')
    else:
        print_colored('Шары НЕ закрыли', '31')

    pyautogui.moveTo(builders_workshop.x, builders_workshop.y)
    time.sleep(0.3)
    r, g, b = image.getpixel((builders_workshop.x, builders_workshop.y))
    builders_workshop.is_closed = check_region(r, g, b)
    if builders_workshop.is_closed:
        print_colored('Строителя закрыли', '32')
    else:
        print_colored('Строителя НЕ закрыли', '31')

    pyautogui.moveTo(dragon_cliffs.x, dragon_cliffs.y)
    time.sleep(0.3)
    r, g, b = image.getpixel((dragon_cliffs.x, dragon_cliffs.y))
    dragon_cliffs.is_closed = check_region(r, g, b)
    if dragon_cliffs.is_closed:
        print_colored('Драконов закрыли', '32')
    else:
        print_colored('Драконов НЕ закрыли', '31')

    pyautogui.moveTo(golem_quarry.x, golem_quarry.y)
    time.sleep(0.3)
    r, g, b = image.getpixel((golem_quarry.x, golem_quarry.y))
    golem_quarry.is_closed = check_region(r, g, b)
    if golem_quarry.is_closed:
        print_colored('Големов закрыли', '32')
    else:
        print_colored('Големов НЕ закрыли', '31')

    pyautogui.moveTo(skeleton_park.x, skeleton_park.y)
    time.sleep(0.3)
    r, g, b = image.getpixel((skeleton_park.x, skeleton_park.y))
    skeleton_park.is_closed = check_region(r, g, b)
    if skeleton_park.is_closed:
        print_colored('Скелетов закрыли', '32')
    else:
        print_colored('Скелетов НЕ закрыли', '31')

    pyautogui.moveTo(goblin_shachts.x, goblin_shachts.y)
    time.sleep(0.3)
    r, g, b = image.getpixel((goblin_shachts.x, goblin_shachts.y))
    goblin_shachts.is_closed = check_region(r, g, b)
    if goblin_shachts.is_closed:
        print_colored('Гоблинов закрыли', '32')
    else:
        print_colored('Гоблинов НЕ закрыли', '31')

def choice_region_to_attack():
    if not goblin_shachts.is_closed:
        return goblin_shachts
    
    if not skeleton_park.is_closed:
        return skeleton_park
    
    if not golem_quarry.is_closed:
        return golem_quarry

    if not dragon_cliffs.is_closed:
        return dragon_cliffs
    
    if not builders_workshop.is_closed:
        return builders_workshop

    if not baloon_lagoon.is_closed:
        return baloon_lagoon
    
    if not wizard_valley.is_closed:
        return wizard_valley
    
    if not barbarian_camp.is_closed:
        return barbarian_camp
    
    # if not capital_peak.is_closed:
    #     return capital_peak


def attack_region(region):
    LMB(region.x-30, region.y+75, 1) # на район
    time.sleep(0.9+random.uniform(0.1, 0.5))
    # LMB(802, 787) # Атака
    time.sleep(0.8)
    army = check_army() # хоги или не хоги

    if army == region.army :
        print('оставляю армию')
        
    else:
        # change_army(region.army)
        print('армию надо поменять')

    time.sleep(0.4)
    LMB(1322+random.uniform(-10, 10), 545) # В атаку
    time.sleep(4)
    attack(region.army, region)



def check_army():
    time.sleep(1)
    screenshot = pyautogui.screenshot() 
    screenshot.save("Skrin.png")  
    unit_Hogs = find_image("unit_Hogs.png")
    unit_Taran = find_image("unit_Taran.png")
    unit_Varvar = find_image("unit_Varvar.png")
    spell_skeleton = find_image("spell_skeleton.png")

    if unit_Hogs == True and unit_Taran == True and unit_Varvar == True and spell_skeleton == True:
        print('Армия хоги')
        return 'hogs'
    else:
        print('Армия не хоги')
        find_and_click("change_army.png")
        find_and_click("delete.png")
        for _ in range(15):
            move_and_click(1152, 803)
            # time.sleep(0.2)
        move_and_click(271, 620)
        move_and_click(446, 798)
        pyautogui.moveTo(1116+random.uniform(-50, 50), 700+random.uniform(-50, 50))
        pyautogui.dragRel(-533 + random.uniform(-15, 15), random.uniform(-20, 10), button='left', duration=0.3 + random.uniform(-0.1, 0.1))
        time.sleep(1)
        for _ in range(3):
            move_and_click(1150, 794)
            # time.sleep(0.2)

        find_and_click("save.png")
        return 'not hogs'





def find_image(image):
    stop = 0
    Find_Place = None
    while stop <= 3:
        screenshot = pyautogui.screenshot() # Сделать скриншот всего экрана
        screenshot.save("Skrin.png")        
        Place = find_piece("Skrin.png", image, 0.8, True)
        if Place:
            Find_Place = remove_close_duplicates(Place, 1)[0] 
            break
        stop+=1
    time.sleep(0.2)
    if not Find_Place:
        print("Не удалось найти картинку после 3 попыток.")
        return False
    x, y = int(Find_Place[0]), int(Find_Place[1])
    print(f"Координаты картинки({image}): {x}, {y}")
    return True








def find_zones_coordinates(zones, radius=40):

    arr = []

    def find_center(center_path, accuracy, out=False):

        center_first = find_piece("screenshot.png", center_path, accuracy)
        center = remove_close_duplicates(center_first, 60)

        if center_path == 'golem_quarry_center.png' and len(center) > 1 :
            center = [center[1]]

        elif center_path == 'baloon_lagoon_center.png' and len(center) > 1:
            center = [center[0][0]-50, center[0][1]]

        if out == False:
            return center
        
        if center:
            print("Найден центр:")
            for idx, (x, y) in enumerate(center):
                print(f"Центр {idx + 1}: Координаты ({x}, {y})")
            
            screenshot_rgb = cv2.imread("screenshot.png", cv2.COLOR_BGR2RGB)
            plt.imshow(screenshot_rgb)

            for idx, (x, y) in enumerate(center):
                plt.scatter(x, y, color='red', marker='o')
                plt.text(x, y, f'Центр {idx + 1}', fontsize=12, color='red')

            plt.show()

            return center
        
        else:
            print("Центра нет...")


    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")

    # screenshot = Image.open("screenshot.png")

    image = screenshot.convert("RGB")
    width, height = image.size

    # Зоны
    if 'green' in zones:
        green_points_1 = []
        for y in range(height-40):
            for x in range(width):

                r, g, b = image.getpixel((x, y))
                if(is_esc == True):
                    return
                
                if (r > 105 and g > 178 and b > 103) and (r < 135 and g < 190 and b < 110) or (r > 124 and g > 175 and b > 87) and (r < 130 and g < 177 and b < 112):
                    green_points_1.append((x, y))

                if (r > 190 and g > 230 and b > 190) and (r < 215 and g < 250 and b < 210):
                    green_points_1.append((x, y))

        green_points = remove_close_duplicates(green_points_1, radius)

        print('точек для высадки:', len(green_points))
        arr.append(green_points)

        # if len(green_points) != 0:
        #     display_dots('screenshot.png', green_points)
        # else:
        #     print('ТОЧКИ ДЛЯ ВЫСАДКИ НЕ НАЙДЕНЫ')

    if 'water' in zones:
        water_points_1 = []
        for y in range(height-40):
            for x in range(width):
                r, g, b = image.getpixel((x, y))
                if ((r > 47 and g > 130 and b > 220) and (r <= 50 and g < 133 and b < 224)) or ((r > 40 and g > 102 and b > 165) and (r <= 50 and g < 128 and b < 210)):
                    water_points_1.append((x, y))

        print('Точки воды:', len(water_points_1))
        water_points = remove_close_duplicates(water_points_1, 20)
        
        arr.append(water_points)

        # if len(water_points) != 0:
        #     display_dots('screenshot.png', water_points)
        # else:
        #     print('ВОДЫ НЕТ')

    # Строения
    if 'rocket' in zones:

        rocket_coordinates_1 = find_piece("screenshot.png", "1_rocket2.png", 0.84)
        rocket_coordinates_12 = find_piece("screenshot.png", "12_rocket.png", 0.92)
        rocket_coordinates_3 = find_piece("screenshot.png", "3_rocket.png", 0.82)
        rocket_coordinates_32 = find_piece("screenshot.png", "3_rocket2.png", 0.89)
        rocket_coordinates_4 = find_piece("screenshot.png", "4_rocket.png", 0.86)
        rocket_coordinates_42 = find_piece("screenshot.png", "4_rocket2.png", 0.88)
        rocket_coordinates_5 = find_piece("screenshot.png", "5_rocket.png", 0.86)
        rocket_coordinates_52 = find_piece("screenshot.png", "5_rocket2.png", 0.86)

        rocket_coordinates_first = rocket_coordinates_1 + rocket_coordinates_12 + rocket_coordinates_3 + rocket_coordinates_32 + rocket_coordinates_4 + rocket_coordinates_42 + rocket_coordinates_5 + rocket_coordinates_52
        
        rocket_coordinates = []
        rocket_coordinates = remove_close_duplicates(rocket_coordinates_first, 60)
        
        arr.append(rocket_coordinates)

        if rocket_coordinates:
            print("Найдены ракеты:")
            # for idx, (x, y) in enumerate(rocket_coordinates):
            #     print(f"Ракета {idx + 1}: Координаты ({x}, {y})")
            
            # screenshot_rgb = cv2.imread("screenshot.png", cv2.COLOR_BGR2RGB)
            # plt.imshow(screenshot_rgb)

            # for idx, (x, y) in enumerate(rocket_coordinates):
            #     plt.scatter(x, y, color='red', marker='o')
            #     plt.text(x, y, f'Ракета {idx + 1}', fontsize=12, color='red')

            # plt.show()

        else:
            print("Ракеты не найдены на скриншоте.")

    if 'gun' in zones:

        gun_coordinates_1 = find_piece("screenshot.png", "1_pushka.png", 0.84)
        gun_coordinates_12 = find_piece("screenshot.png", "1_pushka2.png", 0.92)
        gun_coordinates_2 = find_piece("screenshot.png", "2_pushka.png", 0.82)
        gun_coordinates_22 = find_piece("screenshot.png", "2_pushka2.png", 0.89)
        gun_coordinates_3 = find_piece("screenshot.png", "3_pushka.png", 0.86)
        gun_coordinates_4 = find_piece("screenshot.png", "4_pushka.png", 0.88)

        gun_coordinates_first = gun_coordinates_1 + gun_coordinates_12 + gun_coordinates_2 + gun_coordinates_22 + gun_coordinates_3 + gun_coordinates_4

        gun_coordinates = remove_close_duplicates(gun_coordinates_first, 60)
        arr.append(gun_coordinates)

        if gun_coordinates:
            print("Найдены пушки:")
            for idx, (x, y) in enumerate(gun_coordinates):
                print(f"Пушка {idx + 1}: Координаты ({x}, {y})")
            
            # screenshot_rgb = cv2.imread("screenshot.png", cv2.COLOR_BGR2RGB)
            # plt.imshow(screenshot_rgb)

            # for idx, (x, y) in enumerate(gun_coordinates):
            #     plt.scatter(x, y, color='red', marker='o')
            #     plt.text(x, y, f'Пушка {idx + 1}', fontsize=12, color='red')

            # plt.show()

        else:
            print("Пушки не найдены на скриншоте.")

    if 'inferno' in zones:

        inferno_coordinates_1 = find_piece("screenshot.png", "1_inferno.png", 0.8)
        inferno_coordinates_2 = find_piece("screenshot.png", "2_inferno.png", 0.8)
        inferno_coordinates_3 = find_piece("screenshot.png", "3_inferno.png", 0.8)
        inferno_coordinates_4 = find_piece("screenshot.png", "4_inferno.png", 0.8)

        inferno_coordinates_first = inferno_coordinates_1 + inferno_coordinates_2 + inferno_coordinates_3 + inferno_coordinates_4

        inferno_coordinates = remove_close_duplicates(inferno_coordinates_first, 20)

        for coord in inferno_coordinates:
            coord[0] += 5
            coord[1] += 25

        arr.append(inferno_coordinates)
        
        if inferno_coordinates:

            print("Найдены инферно:")
            # for idx, (x, y) in enumerate(inferno_coordinates):
            #     print(f"Инферно {idx + 1}: Координаты ({x}, {y})")
            
            # screenshot_rgb = cv2.imread("screenshot.png", cv2.COLOR_BGR2RGB)
            # plt.imshow(screenshot_rgb)

            # for idx, (x, y) in enumerate(inferno_coordinates):
            #     plt.scatter(x, y, color='red', marker='o')
            #     plt.text(x, y, f'Инферно {idx + 1}', fontsize=12, color='red')

            # plt.show()

        else:
            print("Инферно не найдены на скриншоте.")

    if 'luk' in zones:

        luk_coordinates_1 = find_piece("screenshot.png", "1_luk.png", 0.8)
        luk_coordinates_2 = find_piece("screenshot.png", "2_luk.png", 0.8)
        luk_coordinates_3 = find_piece("screenshot.png", "3_luk.png", 0.8)
        luk_coordinates_4 = find_piece("screenshot.png", "4_luk.png", 0.8)

        luk_coordinates_first = luk_coordinates_1 + luk_coordinates_2 + luk_coordinates_3 + luk_coordinates_4

        luk_coordinates = remove_close_duplicates(luk_coordinates_first, 20)

        for coord in luk_coordinates:
            coord[0] += 20
            coord[1] += -5

        arr.append(luk_coordinates)

        if luk_coordinates:
            print("Найдены луки:")
            # for idx, (x, y) in enumerate(luk_coordinates):
            #     print(f"Лук {idx + 1}: Координаты ({x}, {y})")
            
            # screenshot_rgb = cv2.imread("screenshot.png", cv2.COLOR_BGR2RGB)
            # plt.imshow(screenshot_rgb)

            # for idx, (x, y) in enumerate(luk_coordinates):
            #     plt.scatter(x, y, color='red', marker='o')
            #     plt.text(x, y, f'Лук {idx + 1}', fontsize=12, color='red')

            # plt.show()

        else:
            print("Лук не найден на скриншоте.")

    # Центры
    if 'skeleton_park' in zones:
        skeleton_park_center = find_center('skeleton_park_center.png', 0.75)
        arr.append(skeleton_park_center)

    elif 'golem_quarry' in zones:
        golem_quarry_center = find_center('golem_quarry_center.png', 0.8)
        arr.append(golem_quarry_center)

    elif 'dragon_cliffs' in zones:
        dragon_cliffs_center = find_center('dragon_cliffs_center.png', 0.8)
        arr.append(dragon_cliffs_center)

    elif 'builders_workshop' in zones:
        builders_workshop_center = find_center('builders_workshop_center.png', 0.8)
        arr.append(builders_workshop_center)

    elif 'baloon_lagoon' in zones:
        baloon_lagoon_center = find_center('baloon_lagoon_center.png', 0.8)
        arr.append(baloon_lagoon_center)

    elif 'wizard_valley' in zones:
        wizard_valley_center = find_center('wizard_valley_center.png', 0.8)
        arr.append(wizard_valley_center)

    elif 'barbarian_camp' in zones:
        barbarian_camp_center = find_center('barbarian_camp_center.png', 0.8)
        arr.append(barbarian_camp_center)

    return arr

def is_army_end(x, y):
    screenshot = pyautogui.screenshot()

    image = screenshot.convert("RGB")
    r, g, b = image.getpixel((x, y))

    if(r == g and g == b):
        return True
    
    return False

def is_attack_end():
    screenshot = pyautogui.screenshot()
    image = screenshot.convert("RGB")
    width, height = image.size

    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            if(is_esc == True):
                return
            
            if (r > 34 and g > 193 and b > 139) and (r < 36 and g < 200 and b < 148):
                return True
            
    return False


def change_akk(num):
    if(num < 5):
        # pyautogui.moveTo(1000, 320+num*120)
        LMB(1000, 320+num*120)
    else:
        pyautogui.moveTo(1089+random.uniform(-10, 10), 798+random.uniform(-1, 1))
        pyautogui.dragRel(random.uniform(-10, 10), -120*(num-4), button='left', duration=0.5)

        # pyautogui.moveTo(1089+random.uniform(-10, 10), 798+random.uniform(-1, 1))
        LMB(1089+random.uniform(-10, 10), 798+random.uniform(-1, 1))

def camera_move(center):

    time.sleep(0.3)
    pyautogui.moveTo(center[0]+random.uniform(-10, 10), center[1]+random.uniform(-10, 10))
    pyautogui.mouseDown()
    pyautogui.moveTo(1440/2+random.uniform(-10, 10), 900/2+random.uniform(-10, 10), duration=random.uniform(1.4, 1.8))
    pyautogui.mouseUp()
    time.sleep(1)


def akk_attack():
    region = choice_region_to_attack()
    attack_region(region)


class Army:
    def __init__(self, x, y):
        self.x = x
        self.y = y

barbarians = Army(189, 853)
taran = Army(306, 853)
hogs = Army(433, 853)
skeleton = Army(559, 849)

def attack(name, region, attack_by_count=0):

    try:
        center = find_zones_coordinates([region.name])[0][0]
        camera_move(center)
    except:
        print('Центр не найден, фиксь баг')

    find_zones_coordinates('green')

    if name == 'hogs' :
        hogs = find_piece('screenshot.png', 'army_hogs.png', 0.8)
        hogs = remove_close_duplicates(hogs, 20)[0]
        hog = Army(hogs[0]+20, hogs[1]+20)
    
        barbarians = find_piece('screenshot.png', 'army_barbarians.png', 0.8)
        barbarians = remove_close_duplicates(barbarians, 20)[0]
        barbarian = Army(barbarians[0]+20, barbarians[1]+20)

        tarans = find_piece('screenshot.png', 'army_taran.png', 0.8)
        tarans = remove_close_duplicates(tarans, 20)[0]
        taran = Army(tarans[0]+20, tarans[1]+20)

        skeletons = find_piece('screenshot.png', 'army_skeleton.png', 0.8)
        skeletons = remove_close_duplicates(skeletons, 20)[0]
        skeleton = Army(skeletons[0]+20, skeletons[1]+20)

        arr = find_zones_coordinates(region.zones)

        green_points = arr[0]
        water_points = arr[1]

        if isinstance(arr[2], list) and isinstance(arr[3], list):
            rocket_points = arr[2] + arr[3]
        elif isinstance(arr[2], list):
            rocket_points = arr[2]
        elif isinstance(arr[3], list):
            rocket_points = arr[3]
        else:
            rocket_points = []  # Оба элемента не являются массивами, создаем пустой массив


        LMB(skeleton.x, skeleton.y)
        i = 0
        while is_esc == False:

            if i < len(rocket_points):
                x, y = rocket_points[i]
            else:
                x, y = get_random_coordinates_outside_zones(green_points, water_points, min_distance=100, min_x=200, max_x=1200, min_y=200, max_y=600)
            i+=1
            LMB(x, y, 1)
            time.sleep(random.uniform(0, 1))
            army_end = is_army_end(skeleton.x, skeleton.y)
            if(army_end):
                break

        LMB(taran.x, taran.y)
        i = 0
        while is_esc == False:
            i+=1
            x, y = random.choice(green_points)
            LMB(x, y, 1)

            time.sleep(random.uniform(0, 1))
            army_end = is_army_end(taran.x, taran.y)
            if(army_end):
                break

        time.sleep(random.uniform(0, 1))
        LMB(barbarian.x, barbarian.y)
        i = 0
        while is_esc == False:
            i+=1
            x, y = random.choice(green_points)
            LMB(x, y, 1)

            time.sleep(random.uniform(0, 0.5))
            army_end = is_army_end(barbarian.x, barbarian.y)
            if(army_end):
                break

        time.sleep(random.uniform(0, 1))
        LMB(hog.x, hog.y)
        i = 0
        while is_esc == False:
            x, y = random.choice(green_points)
            LMB(x, y, 1)
            i+=1
            time.sleep(0.7)
            army_end = is_army_end(hog.x, hog.y)
            if(army_end):
                break

            time.sleep(random.uniform(0, 1))
            
    while True:
        is_end = is_attack_end()
        if is_end == True:
            print('Атака закончилась')
            break

        time.sleep(1)



def is_outside_green_and_water_zones(point, green_points, water_points, min_distance):
    for green_point in green_points:
        if distance(point, green_point) < min_distance:
            return False
    for water_point in water_points:
        if distance(point, water_point) < min_distance:
            return False
    return True


def get_random_coordinates_outside_zones(green_points, water_points, min_distance, min_x, max_x, min_y, max_y):
    while True:
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        if is_outside_green_and_water_zones((x, y), green_points, water_points, min_distance):
            return x, y































# Пример использования
reset_zoom()
drag_mouse(631, 862, 1159, 132, duration=1)
time.sleep(0.3)
find_and_click("Ship.png")
time.sleep(2)
# drag_mouse(478, 700, 508, 504, duration=1)
find_and_click("button_map_raid.png")
time.sleep(0.3)
check_map_raid()
time.sleep(1)

# move_and_click(1135, 663)
# find_and_click("button_Attack.png")
# check_army()

region = choice_region_to_attack()
attack_region(region)
# find_and_click("button_map_exit.png")
# find_and_click("button_exit.png")

attack()