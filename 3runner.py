import readchar
import threading
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep

# number of retries when results are the same (attempts to scroll each time)
try_scoll_empty_retry_limit = 8

# range that new map coordinates are made (in latitude/ longitude) e.g. 3 ~ 115.5 + .3 = 115.8
lat_long_random_range = 2

driver = webdriver.Chrome()

run_scrape=True

start_coord_url = "https://www.google.com/maps/search/Restaurants/@33.803038,-118.0793316,14z/data=!3m1!4b1!4m2!2m1!6e5?entry=ttu"
scrape_coord = None

sites_data_gotten=[]
places_gotten=[]
sites_gotten = []
last_rest = None
last_places_empty = False
last_places_empty_count = 0

def check_key_for_scrape():
    global run_scrape
    global start_coord_url
    key = readchar.readkey()
    # scrape
    if key == "s":
        print("s key rs true")
        run_scrape = True
    # override url and scrape
    if key == "o":
        print("o key rs true")
        start_coord_url = driver.current_url
        scrape_coord = get_scrape_coord_from_url(start_coord_url)
        run_scrape = True
    # terminate
    if key == "t":
        print("t key rs false")
        run_scrape = False
    return key



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


def random_map_move_and_rec():
    global start_coord_url
    global scrape_coord
    new_coord_url_coords_lat = start_coord_url.split("@")[1].split(",")[0]
    new_coord_url_coords_long = start_coord_url.split("@")[1].split(",")[1] 
    rand_ten_lat = random.randrange(0,lat_long_random_range + 1)
    rand_sign_lat = random.randrange(0,2)
    rand_dec_lat = "." + str(rand_ten_lat)
    rand_dec_float_lat = float(rand_dec_lat)
    if rand_sign_lat <1:
        rand_dec_float_lat = -rand_dec_float_lat
    rand_ten_long = random.randrange(0,lat_long_random_range + 1)
    rand_sign_long = random.randrange(0,2)
    rand_dec_long = "." + str(rand_ten_long)
    rand_dec_float_long = float(rand_dec_long)
    if rand_sign_long <1:
        rand_dec_float_long = -rand_dec_float_long
    
    new_coord_url_coords_lat_float = float(new_coord_url_coords_lat)
    new_coord_url_coords_long_float = float(new_coord_url_coords_long)
    new_coord_url_coords_lat_float = new_coord_url_coords_lat_float + rand_dec_float_lat
    new_coord_url_coords_long_float = new_coord_url_coords_long_float + rand_dec_float_long

    new_coord_url = start_coord_url.split("@")[0]+ "@" + str(new_coord_url_coords_lat_float) + "," \
    + str(new_coord_url_coords_long_float) + "," + start_coord_url.split(",")[2]
    print("Create new random url ~ " + new_coord_url)
    start_coord_url = new_coord_url
    driver.get(start_coord_url)
    scroll_down_and_find_places()

def scroll_down_and_find_places():
    global last_rest
    global places_gotten
    global last_places_empty_count
    global last_places_empty
    global run_scrape

    if run_scrape == False:
        return

    
    scroll_down_scroll_list_by_index(5)
    WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME,
             "hfpxzc"))
        )
    place_elems = driver.find_elements(By.CLASS_NAME,'Nv2PK')
    
    place_names_loc = []


    p_index = 0
    places_not_gotten_indexes = []
    # print("all places gotten ~ " + str(places_gotten))
    for place in place_elems:
        # print("finding qBF1PD in place elems")
        placename = place.find_elements(By.CLASS_NAME,"qBF1Pd")[0].get_attribute("innerHTML")
        # print("place name get ~ " + placename)
        place_names_loc.append(placename)
        
        if placename not in places_gotten:
            places_not_gotten_indexes.append(p_index)
        p_index +=1
        
    print("check for list end")
    # look for "You've reached the end of the list"
    list_end_string = "You've reached the end of the list"
    if (len(places_not_gotten_indexes) == 0 and list_end_string in  driver.page_source):
        print("End of List reached.. scroll map")
        random_map_move_and_rec()
        return True
    
    print("all places not gotten indicies ~ " + str(places_not_gotten_indexes))
    if len(places_not_gotten_indexes) == 0:
        print("List scrolling complete... waiting")
        last_places_empty_count += 1
        print("last places not finding more ct ~ " + str(last_places_empty_count))
        if (last_places_empty_count > try_scoll_empty_retry_limit):
            print("last place empty count exceed")
            last_places_empty = True
            random_map_move_and_rec()
            return True
        else:
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
    if (last_places_empty_count < try_scoll_empty_retry_limit):
        print("last places empty ct lt limit ~ " + str(last_places_empty_count))
        scroll_down_and_find_places()

    print("scroll down and find rec")
    return True


def click_restaraunts_and_get_websites(place_index, place_name):
    print("run click restraunts")
    global last_rest
    global run_scrape
    global scrape_coord
    
    if run_scrape == False:
        return
    try:
        print("click place")
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME,
            "hfpxzc")))
        places = driver.find_elements(By.CLASS_NAME,'hfpxzc')
        places[place_index].click()

        phone_get = "n/a"
        try:
            elem0_wrap = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"button[data-tooltip='Copy phone number']")))

            phone_number = elem0_wrap.find_element(By.CLASS_NAME,"Io6YTe").get_attribute("innerHTML")
            print("phone get ~ " + str(phone_number))
            phone_get = phone_number
        except Exception as e:
            print("phone unavailable")

        site_get = "n/a"
        try:
            elem1_wrap = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
            "a[data-item-id='authority']")))
            
            website_div = elem1_wrap.find_element(By.CLASS_NAME,"Io6YTe")

            site_get =  website_div.get_attribute("innerHTML")
        except Exception as e:
            print("site unavailable")
        
        if (last_rest == site_get):
            print("new rest old rest")
            find_and_click_back_button()
            
        last_rest = site_get
        print("got element ~" + site_get)

        if site_get != "n/a" and site_get+"\n" not in sites_gotten:
            sites_gotten.append(site_get+"\n")
            with open("rdata/"+scrape_coord+"-rdata", "a+") as of:
                of.write(f"{place_name},{site_get},{phone_get}" + "\n")
        
        print("loop finish back")
        find_and_click_back_button()
        

    except Exception as e:
        print("Exception caught in click rest ~ "+ str(e))
        find_and_click_back_button()    
        scroll_down_and_find_places()


def get_scrape_coord_from_url(url):
    coords_lat = start_coord_url.split("@")[1].split(",")[0]
    coords_long = start_coord_url.split("@")[1].split(",")[1] 
    coords_lat_trunc = coords_lat.split(".")[0]
    coords_long_trunc = coords_long.split(".")[0]
    if "-" in coords_lat_trunc:
        coords_lat_trunc = "n" + coords_lat_trunc.split("-")[1]
    if "-" in coords_long_trunc:
        coords_long_trunc = "n" + coords_long_trunc.split("-")[1]

    build_scrape_coord = coords_lat_trunc + "-" + coords_long_trunc
    return build_scrape_coord



def loop_scrape():
    print("loop scrape sub func")
    global scrape_coord
    global start_coord_url
    global run_scrape
    global sites_data_gotten
    global sites_gotten
    global places_gotten
    global last_places_empty


    if run_scrape == False:
        return 
    
    driver.get(start_coord_url)
    scrape_coord = get_scrape_coord_from_url(start_coord_url)
    
    try:
        # load last run
        with open("rdata/"+scrape_coord+"-rdata", "r") as of:
            sites_data_gotten = of.readlines()
    except Exception as e:
        print("couldnt open file ")

    for sd in sites_data_gotten:
        sites_gotten.append(sd.split(",")[1])
        places_gotten.append(sd.split(",")[0])

    print("get scrape coord from url ~ " + scrape_coord)
    while last_places_empty == False:
        if run_scrape == False:
            break
        sleep(.2)
        print("scroll and find")
        try:
            scroll_down_and_find_places()
            
        except Exception as e:
            print("top level click except ~ " + str(e))
            scroll_down_and_find_places()
    

def bg_input():
    while True:
        check_key_for_scrape()

def main_loop():
    while True:
        sleep(1)
        print("loop scrape glob main waiting ....")
        loop_scrape()

if __name__ == "__main__":
    print("running main")
    
    thread_key = threading.Thread(target=bg_input)
    thread_key.daemon = False 
    thread_key.start()

    main_loop()

   
                            

        

