import mouse
import time
import keyboard

while 1:
    # scroll lock for starting the process
    keyboard.wait(70)
    keyboard.press(29)
    for i in range(12):
        for j in range(5):
            mouse.move(2610 + 70 * i, 820 + 70 * j, absolute=True, duration=0.01)
            time.sleep(0.02)
            mouse.click()
    keyboard.release(29)

# time.sleep(0.5)
# print(mouse.get_position())