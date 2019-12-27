import mouse
import winsound
import keyboard
import time
# press right shift to turn on and turn off

# key_code for continuously pressing, 42 for shift, 29 for control
key_code = 29
print('POE fusion for RKN running ... on/off: scroll lock')
while 1:
    # scroll lock(70) or F4(62) for starting the process
    on_off_key = 62
    keyboard.wait(on_off_key)
    frequency = 2000  # Set Frequency To 2000 Hertz
    duration = 100  # Set Duration, 1000 ms == 1 second
    for i in range(3):
        winsound.Beep(frequency, duration)

    keyboard.press(key_code)
    while 1:
        if keyboard.is_pressed(on_off_key):
            break
        time.sleep(0.05)
        mouse.click()

    frequency = 2000
    duration = 1000
    winsound.Beep(frequency, duration)
    keyboard.release(key_code)
