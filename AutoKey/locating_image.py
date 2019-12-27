import pyautogui
import threading
import time

def c():
    while 1:
        c_location = pyautogui.locateCenterOnScreen('C:/GithubProject/PythonPractice/AutoKey/currency_pics/c.png', 
            grayscale=False)
        if c_location:
            pyautogui.click(c_location.x, c_location.y)

def ex():
    while 1:
        ex_location = pyautogui.locateCenterOnScreen('C:/GithubProject/PythonPractice/AutoKey/currency_pics/ex.png', 
            grayscale=False)
        if ex_location:
            pyautogui.click(ex_location.x, ex_location.y)

def chisel():
    while 1:
        chisel_location = pyautogui.locateCenterOnScreen('C:/GithubProject/PythonPractice/AutoKey/currency_pics/chisel.png', 
            grayscale=False)
        if chisel_location:
            pyautogui.click(chisel_location.x, chisel_location.y)
    
th_1 = threading.Thread(target=c, daemon=True)
th_2 = threading.Thread(target=ex, daemon=True)
th_3 = threading.Thread(target=chisel, daemon=True)

th_1.start()
th_2.start()
th_3.start()

while 1:
    time.sleep(100)
