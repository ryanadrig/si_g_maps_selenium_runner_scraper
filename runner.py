import site
import readchar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
import os.path


driver = webdriver.Chrome()

sites_gotten=[]


# load last run
try:
    with open("sitesdata", "r") as of:
        sites_gotten = of.readlines()
except Exception as e:
    print("couldnt open file ")

print("sites gotten ~ " + str(sites_gotten))

scroll_index = 1

def find_and_click_back_button():
    print("back button click")
    # sleep(1)
    try:
        back_button = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
            "button[aria-label='Back']"))
        )
        back_button.click()
    except Exception as e:
        print("back button click excepted " + str(e))

# def scroll_down_scroll_list():
#     print("try scroll down")
#     try:
#         scroll_list = WebDriverWait(driver, 2).until(
#             EC.presence_of_element_located((By.CLASS_NAME,
#             "aIFcqe"))
#         )
#         print("Scroll down")
#         driver.execute_script('document.getElementsByClassName("aIFcqe")[0].scrollTop += 1010')
#     except Exception as e:
#         print("scroll down excepted " + str(e))

def scroll_down_scroll_list_by_index(si, gi):
    print("try scroll down")
    print("scrol index ~ " + str(si))
    # sleep(1)
    try:

        # print("Scroll down")
        # win_height = driver.execute_script("return window.innerHeight")
        # print("win height ~ " + str(win_height))
        # print("list element height")
        # print(str(leh))

        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
            "div[aria-label=\"Results for Restaurants\"]"))
        )
        leh = driver.execute_script(
            "return document.getElementsByClassName('hfpxzc')[0].clientHeight"
        )
        #document.querySelector('div[aria-label=\"Results for Restaurants\"]')\
        driver.execute_script(
            f"document.querySelector('div[aria-label=\"Results for Restaurants\"]') \
            .scrollTo({{'top':\
             {(leh * (gi))} }})"
        )
        sleep(1)
    except Exception as e:
        print("scroll down excepted " + str(e))

last_rest = None
def click_restaraunts_and_get_websites(of, reset_scroll):
    print("run click restraunts")
    sleep(1)
    global scroll_index
    global last_rest
    
    WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME,
             "hfpxzc"))
        )
    matchesg = driver.find_elements(By.CLASS_NAME,'hfpxzc')
    if (reset_scroll):
        scroll_index = 1
    else:
         scroll_down_scroll_list_by_index(scroll_index, len(matchesg))

    list_index = 0
    matches_gotten=[]
    
    print("matches g len pre ~ " + str(len(matchesg)))
    # have to refind stale matches
    
    while list_index <= len(matchesg) - 1:
        print("loop matches")
        # sleep(1)
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME,
             "hfpxzc"))
        )
        matches = driver.find_elements(By.CLASS_NAME,'hfpxzc')
        matchesg = matches
        if(len(matches)== 0):
            print("no matches")
            find_and_click_back_button()
            list_index += 1
            break
        else:
            matchesnames = driver.find_elements(By.CLASS_NAME,'Nv2PK')
            mn_index = 0
            for match in matchesnames:
                matchname = match.find_elements(By.CLASS_NAME,"qBF1Pd")[0].get_attribute("innerHTML")
                print("matchname get ~ " + matchname)
                
                if matchname not in matches_gotten:
                    matches_gotten.append(matchname)
                    list_index = mn_index
                    mn_index +=1
                    break

        print("len matches" + str(len(matches)))
        print("list index ~ " + str(list_index))
        # matcheswait = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "hfpxzc")))
        try:
            print("click match")
            matches[list_index].click()
            list_index += 1
            elem_wrap = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
             "a[data-item-id='authority']"))
        )
            data = elem_wrap.find_element(By.CLASS_NAME,"Io6YTe")

            site_get =  data.get_attribute("innerHTML")
            if (last_rest == site_get):
                print("new rest old rest")
                find_and_click_back_button()
                list_index +=1
                continue
            last_rest = site_get
            print("got element ~" + site_get)

            if site_get+"\n" not in sites_gotten:
                sites_gotten.append(site_get+"\n")
                of.write(site_get + "\n")
            else:
                find_and_click_back_button()
                continue
           
            print("loop finish back")
            find_and_click_back_button()
            

        except Exception as e:
            print("Exception caught ~ "+ str(e))
            find_and_click_back_button()
            scroll_down_scroll_list_by_index(scroll_index, len(matchesg))        
            scroll_index +=1
            list_index +=1
            continue
            
    print("matches g len post ~ "+ str(len(matchesg)))
    print("done")
    
    scroll_down_scroll_list_by_index(scroll_index, len(matchesg))
    WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME,
             "hfpxzc"))
        )
    matches = driver.find_elements(By.CLASS_NAME,'hfpxzc')
    if (len(matches) > len(matchesg)):
    # scroll_index +=1
        click_restaraunts_and_get_websites(of, False)
    else:
        scroll_down_scroll_list_by_index(scroll_index, len(matchesg))
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME,
             "hfpxzc"))
        )
        matches = driver.find_elements(By.CLASS_NAME,'hfpxzc')
        if (len(matches) > len(matchesg)):
        # scroll_index +=1
            click_restaraunts_and_get_websites(of, False)
        else:
            print("waiting to continue")

if __name__ == "__main__":
    print("running main")
    driver.get("https://www.google.com/maps/")

    while True:
        key = readchar.readkey()
        if (key == "s"):
            print("scrape")
            html_source = driver.page_source
            with open("sitesdata", "a+") as of:
                try:
                    click_restaraunts_and_get_websites(of, True)
                except Exception as e:
                    print("top level click except ~ " + str(e))
            # print("got source " + html_source)

