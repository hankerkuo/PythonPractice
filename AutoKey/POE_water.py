import keyboard
import winsound
import mouse
import time

from win32gui import GetWindowText, GetForegroundWindow

def check_POE_in_current(func):
    def checking(*args):
        if GetWindowText(GetForegroundWindow()) == 'Path of Exile':
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


# press right shift to turn on and turn off
while 1:
    # TURN ON, block until scroll lock(70) has been stroked
    keyboard.wait(70)
    keyboard.add_hotkey('~', lambda: one_key_water('1, 3, 4, 5'))
    keyboard.add_hotkey('w', lambda: denote_mine())
    keyboard.add_hotkey('F2', lambda: minimize())
    keyboard.add_hotkey('f', lambda: hit_home_scroll())
    # keyboard.add_hotkey('ctrl+~', lambda: sell_item())
    frequency = 2000  # Set Frequency To 2000 Hertz
    duration = 100  # Set Duration, 1000 ms == 1 second
    for i in range(3):
        winsound.Beep(frequency, duration)

    # TURN OFF, block until scroll lock(70) has been stroked
    keyboard.wait(70)
    keyboard.remove_hotkey('~')
    keyboard.remove_hotkey('w')
    keyboard.remove_hotkey('F2')
    keyboard.remove_hotkey('f')
    # keyboard.remove_hotkey('ctrl+~')
    frequency = 2000
    duration = 1000
    winsound.Beep(frequency, duration)





