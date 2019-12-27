import mouse
import keyboard
import time

from mouse import ButtonEvent, MoveEvent, WheelEvent, LEFT, RIGHT, MIDDLE, X, X2, UP, DOWN, DOUBLE
import threading

def denote_mine(key=None):
    while 1:
        # print(mouse.is_pressed(button=key))
        if mouse.is_pressed():
            time.sleep(0.4)
            print('hehe')


# mouse.on_button(lambda y:denote_mine(y), (LEFT,), [LEFT], [DOWN])
mouse_denote = threading.Thread(target=denote_mine, daemon=True)
mouse_denote.start()

while 1:
    time.sleep(1)