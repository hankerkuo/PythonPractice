import keyboard
import winsound
import mouse
import time
import threading

from win32gui import GetWindowText, GetForegroundWindow, GetWindow, SetForegroundWindow
from win32api import PostMessage, SendMessage
from win32con import WM_CHAR, WM_KEYDOWN, GW_CHILD

def check_POE_in_current(func):
    def checking(*args):
        if GetWindowText(GetForegroundWindow()) == 'Path of Exile':
        # if 1:
            func(*args)
        else:
            pass
    return checking

@check_POE_in_current
def sell_item():
    # scroll lock for starting the process
    # holding ctrl and click all the items in the bag (except last 2 column of bag)
    keyboard.press(29)
    for i in range(10):
        for j in range(5):
            mouse.move(2610 + 70 * i, 820 + 70 * j, absolute=True, duration=0.01)
            time.sleep(0.02)
            mouse.click()
    keyboard.release(29)

@check_POE_in_current
def one_key_water(keys):
    keyboard.press_and_release(keys)

@check_POE_in_current
def denote_mine():
    time.sleep(0.4)
    keyboard.press_and_release('d')

@check_POE_in_current
def hit_home_scroll():
    keyboard.press_and_release('i')
    mouse.move(3400, 1000, absolute=True, duration=0.01)
    # mouse.right_click()
    # time.sleep(1)
    # keyboard.press_and_release('i')

@check_POE_in_current
def minimize():
    mouse.move(460, 1425, absolute=True, duration=0.01)
    mouse.click()

@check_POE_in_current
def logout():
    keyboard.press_and_release('esc')
    mouse.move(1718, 623, absolute=True, duration=0.01)

def activate_hotkeys():
    keyboard.add_hotkey('~', lambda: one_key_water('2, 3, 4, 5'))
    # keyboard.add_hotkey('w', lambda: denote_mine())
    # keyboard.add_hotkey('F2', lambda: minimize())
    # keyboard.add_hotkey('F3', lambda: logout())
    # keyboard.add_hotkey('f', lambda: hit_home_scroll())
    # keyboard.add_hotkey('ctrl+Q', lambda: send_message_to_different_channels())
    # keyboard.add_hotkey('ctrl+~', lambda: sell_item())

def deactivate_hotkeys():
    keyboard.remove_hotkey('~')
    # keyboard.remove_hotkey('w')
    # keyboard.remove_hotkey('F2')
    # keyboard.remove_hotkey('F3')
    # keyboard.remove_hotkey('f')
    # keyboard.remove_hotkey('ctrl+Q')
    # keyboard.remove_hotkey('ctrl+~')

@check_POE_in_current
def enter_temp_stop():
    deactivate_hotkeys()
    # restart when the mouse button is stroken
    mouse.wait()
    activate_hotkeys()

def send_message_to_different_channels():
    for i in range(1):
        channel = i + 1
        keyboard.press_and_release(28)
        keyboard.press_and_release(200)
        keyboard.press_and_release(200)
        digits_num = len(str(channel - 1))
        for num in range(digits_num):
            keyboard.press_and_release(14)
        for digit in str(channel):
            keyboard.press_and_release(digit)
        keyboard.press_and_release(28)


def functional_hot_keys():
    # press right shift to turn on and turn off
    # key table -> https://minecraft.gamepedia.com/Key_codes

    activate_hotkeys()
    frequency = 2000  # Set Frequency To 2000 Hertz
    duration = 100  # Set Duration, 1000 ms == 1 second
    for i in range(3):
        winsound.Beep(frequency, duration)
    keyboard.add_hotkey('enter', lambda: enter_temp_stop())


def mouse_lefts(hold='ctrl', on_off_key=62):
    # key_code for continuously pressing, 42 for shift, 29 for control
    if hold == 'ctrl':
        key_code = 29
    elif hold == 'shift':
        key_code = 42
    while 1:
        # scroll lock(70) or F4(62), F5(63) for starting the process
        keyboard.wait(on_off_key)
        frequency = 2000  # Set Frequency To 2000 Hertz
        duration = 50  # Set Duration, 1000 ms == 1 second
        for i in range(2):
            winsound.Beep(frequency, duration)

        keyboard.press(key_code)
        while 1:
            if keyboard.is_pressed(on_off_key):
                break
            time.sleep(0.05)
            mouse.click()

        frequency = 2000
        duration = 100
        winsound.Beep(frequency, duration)
        keyboard.release(key_code)

def key_stroke_in_BG(on_off_key=64):
    # F6(64)
    while 1:
        keyboard.wait(on_off_key)

        frequency = 2000  # Set Frequency To 2000 Hertz
        duration = 100  # Set Duration, 1000 ms == 1 second
        for i in range(2):
            winsound.Beep(frequency, duration)

        hwnd_current = GetForegroundWindow()
        hwndChild = GetWindow(hwnd_current, GW_CHILD)
        while 1:
            # SetForegroundWindow(hwnd_current)
            if keyboard.is_pressed(on_off_key):
                break
            # print(win32gui.GetForegroundWindow())
            # PostMessage(hwndChild, WM_KEYDOWN, ord('E'), 0)
            # SendMessage(hwndChild, WM_KEYDOWN, ord('E'), 0)
            SendMessage(hwnd_current, WM_CHAR, ord('e'), 0 + (0 << 8) + (ord('e') << 16) + (0 << 24))
            # keyboard.press_and_release('e')
            time.sleep(0.05)

        frequency = 2000
        duration = 100
        winsound.Beep(frequency, duration)
    
def stationary_cyclone(on_off_key=64):
    while 1:
        # F6 (64) for starting the process
        keyboard.wait(on_off_key)
        mouse_position = mouse.get_position()
        frequency = 2000  # Set Frequency To 2000 Hertz
        duration = 100  # Set Duration, 1000 ms == 1 second
        for i in range(2):
            winsound.Beep(frequency, duration)
        
        # 18 for key:e
        keyboard.press(18)

        while 1:
            # print(keyboard.is_pressed(18))
            if keyboard.is_pressed(on_off_key):
                break
            # time.sleep(0.001)
            mouse.move(*mouse_position)

        frequency = 2000
        duration = 100
        winsound.Beep(frequency, duration)
        keyboard.release(18)

def flask_every_five_sec(on_off_key=65):
    while 1:
        keyboard.wait(on_off_key)
        frequency = 2000  # Set Frequency To 2000 Hertz
        duration = 100  # Set Duration, 1000 ms == 1 second
        for i in range(2):
            winsound.Beep(frequency, duration)

        time_count = 0.9
        while 1:
            if keyboard.is_pressed(on_off_key):
                break
            if int(time_count) % 5 == 0:
                keyboard.press_and_release('1, 2, 3, 4, 5')
                time_count = 0.9
            time.sleep(0.1)
            time_count += 0.1

        frequency = 2000
        duration = 100
        winsound.Beep(frequency, duration)

if __name__ == '__main__':
    hot_key = threading.Thread(target=functional_hot_keys, daemon=True)
    ctrl_mouse_leftstriking = threading.Thread(target=mouse_lefts, kwargs={'hold': 'ctrl', 'on_off_key': 62}, daemon=True)
    shift_mouse_leftstriking = threading.Thread(target=mouse_lefts, kwargs={'hold': 'shift', 'on_off_key': 63}, daemon=True)
    station_cyclone = threading.Thread(target=stationary_cyclone, kwargs={'on_off_key': 64}, daemon=True)
    auto_flask = threading.Thread(target=flask_every_five_sec, kwargs={'on_off_key': 65}, daemon=True)

    hot_key.start()
    ctrl_mouse_leftstriking.start()
    shift_mouse_leftstriking.start()
    station_cyclone.start()
    auto_flask.start()

    print('POE macro running ...')
    while 1:
        time.sleep(10)



