# import libraries
import random
from selenium import webdriver
from time import sleep
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import numpy as np

chrome_options = Options()
chrome_options.add_argument("--headless")

#define browser
browser = webdriver.Chrome(options = chrome_options)
browser.maximize_window()
address = "https://zingmp3.vn/tim-kiem/tat-ca?q="
browser.get(address)

# read the data from database 
df = pd.read_csv("Failure.csv")

def take_title(num):
    title = str(list(df.title.loc[df.index==num]))[2:-2]
    return title

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

df["Genre"] = None
df["Lyric"] = None
number_song = 0
total_song  = len(df.index)

while number_song <= 50:
    try:
        title = take_title(number_song)
        fill_input = browser.find_element_by_xpath('//*[@id="root"]/div[1]/header/div/div[1]/form/div/div/input')
        fill_input.send_keys(title)
        fill_input.send_keys(Keys.ENTER)

        sleep(0.5)
        # have_song = browser.find_element_by_xpath('//*[@id="body-scroll"]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]')
        # print(len(have_song))

        list_song = browser.find_element_by_xpath('//*[@id="body-scroll"]/div[1]/div/div[2]/div/div[1]')
        # press the right-mouse to display list
        ActionChains(browser).context_click(list_song).perform()
        sleep(0.2)
        
        #object of ActionChains
        #identify element
        sing = browser.find_element_by_xpath('//*[@id="react-cool-portal"]/div/div/div/ul[1]/div/div[1]/div[2]/a')
        #hover over singer element
        move_to_hover = ActionChains(browser).move_to_element(sing)
        move_to_hover.perform()
        sleep(0.2)

        #identify sub menu element
        song_info_ubmenu = browser.find_elements_by_xpath('//*[@id="react-cool-portal"]/div/div/div/ul[1]/div/div[2]/div/div')

        for item in song_info_ubmenu:
            
            if str(item.find_element_by_class_name("subtitle").text)[0] == "T":
                
                contents = item.find_element_by_class_name('content')
                
                df["Genre"].loc[df.index==number_song]=(contents.text)
        
        lyris_button = browser.find_element_by_xpath('//*[@id="react-cool-portal"]/div/div/div/ul[2]/div/div/button[2]')
        lyris_button.click()
        lyrics_area = browser.find_elements_by_xpath('//*[@id="react-cool-portal"]/div[2]/div/div/div/div/div[1]')
        sleep(0.2)

        # Add the lyric to df
        df["Lyric"].loc[df.index==number_song] = lyrics_area[0].text
        fill_input.clear()
        number_song = number_song + 1
            
    except:
        fill_input.clear()
        print("error")
        number_song = number_song + 1

df.to_csv("data.csv")        
print(df.head(50))
browser.close()
browser.quit()