import site
import readchar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import os.path


driver = webdriver.Chrome()


def scroll_down_scroll_list(scroll_index):
    print("try scroll down")
    try:

        # print("Scroll down")
        # win_height = driver.execute_script("return window.innerHeight")
        # print("win height ~ " + str(win_height))
        # print("list element height")
        leh = driver.execute_script(
            "return document.getElementsByClassName('hfpxzc')[0].clientHeight"
        )
        # print(str(leh))

        #document.querySelector('div[aria-label=\"Results for Restaurants\"]')\
        driver.execute_script(
            f"document.querySelector('div[aria-label=\"Results for Restaurants\"]') \
            .scrollTo({{'top':\
             {(leh * 4) * scroll_index} }})"
        )
    except Exception as e:
        print("scroll down excepted " + str(e))


if __name__ == "__main__":
    print("running main")
    driver.get("https://www.google.com/maps/")

    scroll_index = 1
    while True:
        key = readchar.readkey()
        if (key == "s"):
            scroll_down_scroll_list(scroll_index)
            scroll_index += 1
            print("scrape")

    
