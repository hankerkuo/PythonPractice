import keyboard
import winsound
import mouse
import time


# press right shift to turn on and turn off
while 1:
    # TURN ON, block until scroll lock(70) has been stroked
    keyboard.wait(70)

    frequency = 2000  # Set Frequency To 2000 Hertz
    duration = 100  # Set Duration, 1000 ms == 1 second
    for i in range(3):
        winsound.Beep(frequency, duration)

    while 1:
        if keyboard.is_pressed(70):
            break
        keyboard.press_and_release('1, 2, 3, 4, 5, R')
        time.sleep(4)

    # TURN OFF, block until scroll lock(70) has been stroked
    frequency = 2000
    duration = 1000
    winsound.Beep(frequency, duration)





