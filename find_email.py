

import readchar
import threading
import random
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep



options = webdriver.ChromeOptions()
# options.add_argument("enable-automation");
# options.add_argument("--headless");
# options.add_argument("--window-size=1920,1080");
# options.add_argument("--no-sandbox");
options.add_argument("--disable-extensions");
options.add_argument("--dns-prefetch-disable");
options.add_argument("--disable-gpu");

driver = webdriver.Chrome(options= options)

driver.set_page_load_timeout(6)

linesites = []

with open("agg_data_san_rd.txt", "r") as f:
    linesites = f.readlines()


sites = []
for line in linesites:
    # print("ls ~ " + line)
    sites.append(line.split(",")[1])

# print("Sites " + str(sites))

"""
Test Stubs
"""
# sites = ["knowlwoodrestaurants.com/"]
# rec_file = "poss_emails_for_sites_TO0"


rec_file = "poss_emails_for_sites"

def get_site_poss(site_content):
    poss = []
    for bs in ps.split(">"):
        if "@" in bs.split("<")[0]:
            if len(bs.split("<")[0]) < 88 and len(bs.split("<")[0]) > 5:
        
                poss.append(bs.split("<")[0])


    if "email" in ps.lower():
        for chunk in ps.lower().split("email"):
            s=("".join(chunk[0:55])) 
            # print( "email splist appending " + s )
            poss.append(s)
    return poss

def record_poss(site,poss):
    pos_string = "poss for site ~ " +site+" ~~ " + str(poss)
    print(pos_string)
    
    with open(rec_file, "a+") as of:
        of.write(pos_string + "\n\n")
        of.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")



    

scount = 0
for site in sites:
    scount+=1
    if (scount < 1168):
        continue

    sg = None
    try:
        sg = driver.get("https://" + site)
        ps = driver.page_source

        def compare_source(driver):
            try:
                return ps != driver.page_source
            except WebDriverException:
                pass
        
        # WebDriverWait(driver, 6).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR,
        #         "div"))
        #     )
        WebDriverWait(driver,8).until(compare_source)

        sp = get_site_poss(ps)
        record_poss(site, sp)

    except Exception as e:
        print("exc caught ~ " + str(e))
        continue

    
    
    try:
        try_contact_url = "https://" + site + "/contact"
        sg = driver.get(try_contact_url)

        def compare_source(driver):
                try:
                    return ps != driver.page_source
                except WebDriverException:
                    pass
            
        # WebDriverWait(driver, 6).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR,
        #         "div"))
        #     )
        WebDriverWait(driver,8).until(compare_source)
        
        response = requests.get(try_contact_url)

        response_code = response.status_code
        if response_code == 200:
            with open(rec_file, "a+") as of:
                of.write("~shc~" + try_contact_url + "~shc~")

    except Exception as e:
        print("exc caught ~ " + str(e))
        continue

    ps = driver.page_source
    sp = get_site_poss(ps)
    record_poss(site, sp)




    # sleep(3)
    # continue