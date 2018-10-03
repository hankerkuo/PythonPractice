from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyHook
import pythoncom

# driver = webdriver.Edge()
driver = webdriver.Chrome()
driver.set_window_position(-1866, 0)
driver.maximize_window()
# print(driver.get_window_position())
# driver.get(site)
driver.get('https://tw.dictionary.search.yahoo.com')
naer = "window.open('http://terms.naer.edu.tw/')"
driver.execute_script(naer)
daum = "window.open('http://alldic.daum.net/index.do?dic=ch/')"
driver.execute_script(daum)

# background = driver.find_element_by_tag_name('body')
# while 1:
#     background.send_keys(Keys.CONTROL + Keys.HOME)

def get_search_name(index):
    if index == '1':
        return 'p'
    elif index == '2':
        return 'q'
    elif index == '3':
        return 'q'

stop_searching = False
while stop_searching is False:
    print("Input vocabulary or website index (1: yahoo 字典, 2: Daum사전, 3: 國家教育研究院雙語辭典)")
    vocab = input()
    if len(vocab) < 1:
        print("input error, please input again")
        continue
    if str.isdigit(vocab[0]):
        driver.switch_to.window(driver.window_handles[int(vocab[0]) - 1])
        search_name = get_search_name(vocab[0])
        continue
    if vocab == 'exit':
        stop_searching = True
    else:
        background = driver.find_element_by_tag_name('body')
        background.send_keys(Keys.CONTROL + Keys.HOME)
        try:
            wait = WebDriverWait(driver, 5)
            elem = wait.until(EC.element_to_be_clickable((By.NAME, search_name)))
        except:
            print("website connction error, please try again")
            continue
        # elem = driver.find_element_by_name(search_name)
        elem.clear()
        elem.send_keys(vocab)
        # elem.send_keys(Keys.RETURN)
        elem.submit()
        # time.sleep(1)
        if '抱歉，目前查無相關資料' in driver.page_source:
            print('no result, back to previous page')
            driver.back()
driver.close()
