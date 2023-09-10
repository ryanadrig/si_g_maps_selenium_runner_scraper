import site
import readchar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
# Get the currently displayed page's HTML source


sites_gotten = []

def click_restaraunts_and_get_websites(of):
    matchesg = driver.find_elements(By.CLASS_NAME,'hfpxzc')
    index = 0
    print("matches g len ~ " + str(len(matchesg)))
    # have to refind stale matches
    while index <= len(matchesg) - 1:
    # for m in matchesg:
        matches = driver.find_elements(By.CLASS_NAME,'hfpxzc')
        # matcheswait = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "hfpxzc")))
        matches = driver.find_elements(By.CLASS_NAME,'hfpxzc')
        try:
            matches[index].click()
            element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
             "a[data-item-id='authority']"))
        )
            data = element.find_element(By.CLASS_NAME,"Io6YTe")

            site_get =  data.get_attribute("innerHTML")
            print("got element ~" + site_get)

            if site_get not in sites_gotten:
                sites_gotten.append(site_get)
                of.write(site_get + "\n")
            index += 1
            back_button = driver.find_element(By.CSS_SELECTOR,
            "button[aria-label='Back']")
            back_button.click()

        except Exception as e:
            print("Exception caught ~ "+ str(e))
    print("matches g len ~ "+ str(len(matchesg)))
    print("done")
    # matches[0].click()
    # element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-item-id='authority']"))
    # )
    # data = element.find_element(By.CLASS_NAME,"Io6YTe")

    # print("got element ~" + data.get_attribute("innerHTML"))
if __name__ == "__main__":
    print("running main")
    driver.get("https://www.google.com/maps/")

    while True:
        key = readchar.readkey()
        if (key == "s"):
            print("scrape")
            html_source = driver.page_source
            with open("sitesdata", "a+") as of:
                click_restaraunts_and_get_websites(of)
            # print("got source " + html_source)

