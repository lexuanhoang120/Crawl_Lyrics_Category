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

chrome_options = Options()
# chrome_options.add_argument("--headless")


#define browser
browser = webdriver.Chrome(options = chrome_options,executable_path="chromedriver")
browser.maximize_window()
address = "https://zingmp3.vn/tim-kiem/tat-ca?q="
browser.get(address)

# read the data from database 
df = pd.read_csv("Failure.csv")

def take_title(num):
    title = str(list(df.title.loc[df.index==num]))[2:-2]
    return title

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
df["Lyrics"] = None
numer_song = 0
total_song  = len(df.index)
print(total_song)

while numer_song <= 1:
    try:
        title = take_title(numer_song)
        fill_input = browser.find_element_by_xpath('//*[@id="root"]/div[1]/header/div/div[1]/form/div/div/input')
        fill_input.send_keys(title)
        fill_input.send_keys(Keys.ENTER)
        sleep(random.randint(1,5)/5)

        play = browser.find_element_by_class_name('zm-actions-container')
        play.click()
        sleep(random.randint(1,5)/5)
        more = browser.find_element_by_xpath('//*[@id="np_menu"]/button')
        more.click()
        sleep(random.randint(1,5)/5)
        
        #object of ActionChains
        #identify element

        sing = browser.find_element_by_xpath('//*[@id="np_menu"]/div/div/div/ul[1]/div/div[1]/div[2]/a')
        #hover over singer element
        move_to_hover = ActionChains(browser).move_to_element(sing)
        move_to_hover.perform()
        sleep(random.randint(1,5)/10)
        
        #identify sub menu element
        song_info_ubmenu = browser.find_elements_by_xpath('//*[@id="np_menu"]/div/div/div/ul[1]/div/div[2]/div/div')
        
        for item in song_info_ubmenu:
            if str(item.find_element_by_class_name("subtitle").text)[0] == "T":
                contents = item.find_element_by_class_name('content')
                print(contents.text)
                df["Lyrics"].loc[df.index==numer_song] = contents.text
        

        fill_input.clear()
        numer_song = numer_song + 1
            
    except:
        print("error")
        numer_song = numer_song + 1

df.to_csv("genre.csv")    

print(df.head())
browser.close()
browser.quit()