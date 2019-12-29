import pyautogui
import threading
import time
import mouse

def c():
    time.sleep(2)
    while 1:
        c_location = pyautogui.locateAllOnScreen('currency_pics/c_lab.png', 
            grayscale=False)
        if c_location:
            now_pt = [0, 0]
            character = (1719, 632)
            for location in c_location:
                corr = pyautogui.center(location)
                mouse.move(corr.x - now_pt[0], corr.y - now_pt[1], absolute=True, duration=0.01)
                time.sleep(0.1)
                mouse.click()
                time.sleep(0.5)
                now_pt[0] = corr.x - 1719
                now_pt[1] = corr.y - 632

def ex():
    while 1:
        ex_location = pyautogui.locateCenterOnScreen('currency_pics/ex_lab.png', 
            grayscale=False)
        if ex_location:
            pyautogui.click(ex_location.x, ex_location.y)

def fusing():
    while 1:
        fusing_location = pyautogui.locateCenterOnScreen('currency_pics/fusing_lab.png', 
            grayscale=False)
        if fusing_location:
            pyautogui.click(fusing_location.x, fusing_location.y)
    
th_1 = threading.Thread(target=c, daemon=True)
th_2 = threading.Thread(target=ex, daemon=True)
th_3 = threading.Thread(target=fusing, daemon=True)

th_1.start()
th_2.start()
th_3.start()

while 1:
    time.sleep(100)
