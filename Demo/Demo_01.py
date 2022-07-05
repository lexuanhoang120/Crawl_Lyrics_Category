from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.chrome.options import Options

import csv
import pandas as pd
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='chromedriver',options=chrome_options)





url = 'https://mp3.zing.vn/'
driver.get(url)

search_field = driver.find_element_by_xpath('//*[@id="sug"]/form/input')
search_field.click()

search_query = "snh yeu em"
search_field.send_keys(search_query)

search_field.send_keys(Keys.RETURN)

action = ActionChains(driver)
action.context_click(driver.find_element_by_xpath('//*[@id="body-scroll"]/div[1]/div/div/div[1]/div/div[2]/div/span/span[1]/span')).perform()
sleep(1)

lyrics_button = driver.find_element_by_xpath('//*[@id="react-cool-portal"]/div/div/div/ul[2]/div/div/button[2]')
lyrics_button.click()

lyrics = driver.find_elements_by_xpath('//*[@id="react-cool-portal"]/div[2]/div/div/div/div/div[1]') 
sleep(1)

lst = ""

lst = lyrics[0].text


# lst = lst + l.text
print(lst)

driver.close()


    
    

    


