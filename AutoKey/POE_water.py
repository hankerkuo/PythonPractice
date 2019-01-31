import keyboard
import winsound
import mouse
import time


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


# press right shift to turn on and turn off
while 1:
    # TURN ON, block until scroll lock(70) has been stroked
    keyboard.wait(70)
    keyboard.add_hotkey('~', lambda: keyboard.press_and_release('1, 2, 3, 4, 5, R'))
    keyboard.add_hotkey('ctrl+~', lambda: sell_item())
    frequency = 2000  # Set Frequency To 2000 Hertz
    duration = 100  # Set Duration, 1000 ms == 1 second
    for i in range(3):
        winsound.Beep(frequency, duration)

    # TURN OFF, block until scroll lock(70) has been stroked
    keyboard.wait(70)
    keyboard.remove_hotkey('~')
    keyboard.remove_hotkey('ctrl+~')
    frequency = 2000
    duration = 1000
    winsound.Beep(frequency, duration)





