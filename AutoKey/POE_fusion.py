import mouse
import winsound
import keyboard
import time
# press right shift to turn on and turn off

# key_code for continuously pressing, 42 for shift, 29 for control
key_code = 42
print('POE fusion for RKN running ... on/off: scroll lock')
while 1:
    # scroll lock for starting the process
    keyboard.wait(70)
    frequency = 2000  # Set Frequency To 2000 Hertz
    duration = 100  # Set Duration, 1000 ms == 1 second
    for i in range(3):
        winsound.Beep(frequency, duration)

    keyboard.press(key_code)
    while 1:
        if keyboard.is_pressed(70):
            break
        time.sleep(0.05)
        mouse.click()

    frequency = 2000
    duration = 1000
    winsound.Beep(frequency, duration)
    keyboard.release(key_code)
