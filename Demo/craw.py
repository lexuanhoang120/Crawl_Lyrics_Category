from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import csv

driver = webdriver.Chrome()
# sleep(2)

url = 'https://mp3.zing.vn/'
driver.get(url)
# sleep(3)

search_field = driver.find_element_by_xpath('//*[@id="sug"]/form/input')
search_field.click()

search_query = "Duyen phan"
search_field.send_keys(search_query)
# sleep(3)

search_field.send_keys(Keys.RETURN)
# sleep(2)

action = ActionChains(driver)
action.context_click(driver.find_element_by_xpath('//*[@id="body-scroll"]/div[1]/div/div/div[1]/div/div[2]/div/span/span[1]/span')).perform()
sleep(1)

# # check_song_field = driver.find_element_by_xpath('//*[@id="react-cool-portal"]/div/div/div/ul[1]/div/div[1]/div[2]/a/div/span/span/span[1]/span')
# # action.move_to_element(check_song_field).perform()
# action.context_click(driver.find_element_by_xpath('//*[@id="react-cool-portal"]/div/div/div/ul[2]/div/div/button[2]')).perform()

lyrics_button = driver.find_element_by_xpath('//*[@id="react-cool-portal"]/div/div/div/ul[2]/div/div/button[2]')
lyrics_button.click()

lyrics = driver.find_elements_by_xpath('//*[@id="react-cool-portal"]/div[2]/div/div/div/div/div[1]/textarea') 

song_lyrics=[]
for l in lyrics:
    print(l.text)
    song_lyrics.append(l)
print(song_lyrics)


    


