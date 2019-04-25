import mouse
import winsound
import keyboard
import time
# press right shift to turn on and turn off

# key_code for continuously pressing, 42 for shift, 29 for control
key_code = 42
print('horse game running ... on/off: scroll lock')
while 1:
    # scroll lock for starting the process
    keyboard.wait(70)
    frequency = 2000  # Set Frequency To 2000 Hertz
    duration = 100  # Set Duration, 1000 ms == 1 second
    for i in range(3):
        winsound.Beep(frequency, duration)

    while 1:
        if keyboard.is_pressed(70):
            break
        time.sleep(0.3)
        keyboard.press_and_release('j, k')
        time.sleep(0.3)
        keyboard.press_and_release('h, l')

    frequency = 2000
    duration = 1000
    winsound.Beep(frequency, duration)
    keyboard.release(key_code)
