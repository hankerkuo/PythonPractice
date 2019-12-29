import time

import cv2
import mss
import numpy as np
import pyautogui
import threading

def processing_time(func):
    def func_final(*args):
        start = time.time()
        func(*args)
        print('processing time:{}'.format(time.time() - start))
    return func_final

@processing_time
def find_using_PAG():
    with mss.mss() as sct:
        filename = sct.shot()
        print(filename)
        # result = pyautogui.locateCenterOnScreen('C:\GithubProject\PythonPractice\AutoKey\currency_pics\c.png', region=(0,0, 500, 500))
        result = pyautogui.locate('C:\GithubProject\PythonPractice\AutoKey\currency_pics\c.png', filename)
        print(result)

@processing_time
def find_using_mss_openCV(img):
    with mss.mss() as sct:
        # monitor = {"top": 0, "left": 0, "width": 2255, "height": 1503}
        monitor = {"top": 500, "left": 500, "width": 1000, "height": 1000}
        screen = np.array(sct.grab(monitor))[:, :, :3]
        # print(screen[..., 3])

    def find_c():
            print('start finding ... ')
            cv2.matchTemplate(screen, img, cv2.TM_CCOEFF_NORMED)
            print('end finding ... ')
    def find_ex():
            cv2.matchTemplate(screen, img, cv2.TM_CCOEFF_NORMED)
    threads = []
    for i in range(10):
        threads.append(threading.Thread(target=find_c, daemon=True))
        threads[-1].start()
    for thread in threads:
        thread.join()
    # for i in range(100):
    #     find_c()
        

    
find_using_PAG()

img = cv2.imread('C:\GithubProject\PythonPractice\AutoKey\currency_pics\c.png')

find_using_mss_openCV(img)