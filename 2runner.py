import readchar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep


driver = webdriver.Chrome()

run_scrape=True

sites_data_gotten=[]
places_gotten=[]
last_rest = None
sites_gotten = []
last_places_empty = False


last_places_empty_count = 0

def check_key_for_scrape():
    global run_scrape
    key = readchar.readkey()
    if key == "s":
        print("s key rs true")
        run_scrape = True
    if key == "t":
        print("t key rs false")
        run_scrape = False
    return key



# load last run
try:
    with open("sitesdata", "r") as of:
        sites_data_gotten = of.readlines()
except Exception as e:
    print("couldnt open file ")

print("sites gotten ~ " + str(sites_data_gotten))

for sd in sites_data_gotten:
    sites_gotten.append(sd.split(",")[1])
    places_gotten.append(sd.split(",")[0])


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



def scroll_down_scroll_list_by_index(matches_len):
    print("try scroll down")

    try:

        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
            "div[aria-label=\"Results for Restaurants\"]"))
        )
        leh = driver.execute_script(
            "return document.getElementsByClassName('hfpxzc')[0].clientHeight"
        )

        driver.execute_script(
            f"document.querySelector('div[aria-label=\"Results for Restaurants\"]') \
            .scrollTo({{'top': {leh * matches_len} }})")
        
    except Exception as e:
        print("scroll down excepted " + str(e))



def scroll_down_and_find_places():
    global last_rest
    global places_gotten
    global last_places_empty_count
    global last_places_empty

    
    scroll_down_scroll_list_by_index(5)
    WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME,
             "hfpxzc"))
        )
    place_elems = driver.find_elements(By.CLASS_NAME,'Nv2PK')
    
    place_names_loc = []

    p_index = 0
    places_not_gotten_indexes = []
    print("all places gotten ~ " + str(places_gotten))
    for place in place_elems:
        placename = place.find_elements(By.CLASS_NAME,"qBF1Pd")[0].get_attribute("innerHTML")
        # print("place name get ~ " + placename)
        place_names_loc.append(placename)
        
        if placename not in places_gotten:
            places_not_gotten_indexes.append(p_index)
        p_index +=1
        
    
    print("all places not gotten indicies ~ " + str(places_not_gotten_indexes))
    if len(places_not_gotten_indexes) == 0:
        print("List scrolling complete... waiting")
        last_places_empty_count += 1
        if (last_places_empty_count >3):
            print("last places not finding more")
            last_places_empty = True

        scroll_down_scroll_list_by_index(len(place_names_loc))
        scroll_down_and_find_places()
    else:
        last_places_empty_count = 0

    print("Get places in places not gotten indicies")
    print("place names loc ~ " + str(place_names_loc))
    print("place names loc indicies" + str(places_not_gotten_indexes))
    gpi_index = 0
    for place_index in places_not_gotten_indexes:
        print("loop place not gotten")
        if place_names_loc[place_index] not in places_gotten:
            print("found place not in gotten")
            last_places_empty_count +=1
            places_gotten.append(place_names_loc[place_index])
            click_restaraunts_and_get_websites(place_index, place_names_loc[place_index])
        gpi_index +=1 

    print("places not gotten loop complete")
    if (last_places_empty_count < 3):
        print("last places empty ct lt 3")
        scroll_down_and_find_places()

    print("scroll down and find done")


def click_restaraunts_and_get_websites(place_index, place_name):
    print("run click restraunts")
    global last_rest
    try:
        print("click place")
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME,
             "hfpxzc"))
        )
        places = driver.find_elements(By.CLASS_NAME,'hfpxzc')
        

        places[place_index].click()

        elem0_wrap = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"button[data-tooltip='Copy phone number']")))

        phone_number = elem0_wrap.find_element(By.CLASS_NAME,"Io6YTe").get_attribute("innerHTML")
        print("phone get ~ " + str(phone_number))


        elem1_wrap = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
            "a[data-item-id='authority']"))
    )
               

        website_div = elem1_wrap.find_element(By.CLASS_NAME,"Io6YTe")

        site_get =  website_div.get_attribute("innerHTML")
        if (last_rest == site_get):
            print("new rest old rest")
            find_and_click_back_button()
            
        last_rest = site_get
        print("got element ~" + site_get)

        if site_get+"\n" not in sites_gotten:
            sites_gotten.append(site_get+"\n")
            of.write(f"{place_name},{site_get},{phone_number}" + "\n")
        
        print("loop finish back")
        find_and_click_back_button()
        

    except Exception as e:
        print("Exception caught in click rest ~ "+ str(e))
        find_and_click_back_button()    
        scroll_down_and_find_places()

   
    
if __name__ == "__main__":
    print("running main")
    driver.get("https://www.google.com/maps/")

    while True:
        key = check_key_for_scrape()
        if (key == "s"):
            print("scrape")
            run_scrape = True
            last_places_empty = False
            html_source = driver.page_source
            with open("sitesdata", "a+") as of:
                while last_places_empty == False:
                    try:
                        scroll_down_and_find_places()
                    except Exception as e:
                        print("top level click except ~ " + str(e))
            

        

