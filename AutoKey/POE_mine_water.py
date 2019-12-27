import keyboard
import winsound
import mouse
import time
import threading

from win32gui import GetWindowText, GetForegroundWindow
from mouse import LEFT, RIGHT, MIDDLE, UP, X, X2, DOWN, DOUBLE

def check_POE_in_current(func):
    def checking(*args):
        if GetWindowText(GetForegroundWindow()) == 'Path of Exile':
        # if 1:
            func(*args)
        else:
            pass
    return checking

@check_POE_in_current
def one_key_water(keys):
    keyboard.press_and_release(keys)

@check_POE_in_current
def denote_mine():
    time.sleep(0.4)
    keyboard.press_and_release('d')

def denote_mine_for_mouse(key):
    frequency = 5000  # Set Frequency To 2000 Hertz
    duration = 100  # Set Duration, 1000 ms == 1 second
    for i in range(2):
        winsound.Beep(frequency, duration)
    while 1:
        if mouse.is_pressed(button=key) and GetWindowText(GetForegroundWindow()) == 'Path of Exile':
        # if mouse.is_pressed(button=key):
            time.sleep(0.4)
            keyboard.press_and_release('d')

@check_POE_in_current
def hit_home_scroll():
    keyboard.press_and_release('i')
    mouse.move(3400, 1000, absolute=True, duration=0.01)

@check_POE_in_current
def minimize():
    mouse.move(460, 1425, absolute=True, duration=0.01)
    mouse.click()

def activate_hotkeys(mine_hotkey, flask_hotkey, flasks_use):
    '''for mine'''
    # if it's keyboard event
    if mine_hotkey[0] == keyboard.add_hotkey:
        keyboard.add_hotkey(mine_hotkey[1], lambda: denote_mine())
    # if it's mouse event
    elif mine_hotkey[0] == mouse.on_button:
        pass

    '''for flask'''
    # if it's keyboard event
    if flask_hotkey[0] == keyboard.add_hotkey:
        keyboard.add_hotkey(flask_hotkey[1], lambda x: one_key_water(x), (flasks_use,))
    # if it's mouse event
    elif flask_hotkey[0] == mouse.on_button:
        flask_hotkey[0](lambda x:one_key_water(x), (flasks_use,), [flask_hotkey[1]], [UP])


def deactivate_hotkeys(mine_hotkey, flask_hotkey):
    '''for mine'''
    # if it's keyboard event
    if mine_hotkey[0] == keyboard.add_hotkey:
        keyboard.remove_hotkey(mine_hotkey[1])
    # if it's mouse event
    elif mine_hotkey[0] == mouse.on_button:
        pass

    '''for flask'''
    # if it's keyboard event
    if flask_hotkey[0] == keyboard.add_hotkey:
        keyboard.remove_hotkey(flask_hotkey[1])
    # if it's mouse event
    elif flask_hotkey[0] == mouse.on_button:
        mouse.unhook_all()
    
@check_POE_in_current
def enter_temp_stop():
    deactivate_hotkeys(mine_hotkey, flask_hotkey)
    # restart when the mouse button is stroken
    mouse.wait()
    activate_hotkeys(mine_hotkey, flask_hotkey, flasks_use)

def define_keyboard_mouse(user_input):
    if user_input == 'mouse_left':
        hotkey = (mouse.on_button, LEFT)
    elif user_input == 'mouse_right':
        hotkey = (mouse.on_button, RIGHT)
    elif user_input == 'mouse_middle':
        hotkey = (mouse.on_button, MIDDLE)
    elif user_input == 'mouse_X':
        hotkey = (mouse.on_button, X)
    elif user_input == 'mouse_X2':
        hotkey = (mouse.on_button, X2)
    elif user_input[:8] == 'keyboard':
        code = user_input.split('_')[1]
        hotkey = (keyboard.add_hotkey, int(code))
    return hotkey

# key table -> https://minecraft.gamepedia.com/Key_codes

print('Free your finger, POE, By PIKO')

with open('configs.txt', 'r') as config:
    meet = 0
    for line in config.readlines():
        if line[0] in ['#', '\n']:
            continue
        if line[-1] == '\n':
            line = line[:-1]
        if meet == 0:
            mine_key = line.strip()
            meet += 1
        elif meet == 1:
            flask_key = line.split(',')[0].strip()
            flasks_use = line.split(',')[1].strip()

# print(mine_key, flask_key, flasks_use)

# mine_key = input('Enter your mine key code: ')
mine_hotkey = define_keyboard_mouse(mine_key)

# flask_key = input('Enter your flask key code: ')
flask_hotkey = define_keyboard_mouse(flask_key)

# flasks_use = input('Enter your auto flask: ')

flask_seq = []
for flask in flasks_use:
    flask_seq.append(flask)
flasks_use = ','.join(flask_seq)

def main_thread():
    activate_hotkeys(mine_hotkey, flask_hotkey, flasks_use)
    frequency = 2000  # Set Frequency To 2000 Hertz
    duration = 100  # Set Duration, 1000 ms == 1 second
    for i in range(2):
        winsound.Beep(frequency, duration)
    keyboard.add_hotkey('enter', lambda: enter_temp_stop())

main = threading.Thread(target=main_thread, daemon=True)
main.start()

time.sleep(0.5)

if mine_hotkey[0] == mouse.on_button:
    mine_for_mouse = threading.Thread(target=denote_mine_for_mouse, args=(mine_hotkey[1],), daemon=True)
    mine_for_mouse.start()

print('Activating ... ')

played_hours = 0
while 1:
    time.sleep(3600)
    played_hours += 1
    print('you have played POE for {} hours! What a nerdy guy!'.format(played_hours))
