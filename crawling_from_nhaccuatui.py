# import libraries
import random
from selenium import webdriver
from time import sleep
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_argument("--headless")

#define browser
browser = webdriver.Chrome(options = chrome_options, executable_path="driver\chromedriver.exe")
browser.maximize_window()
address = "https://www.nhaccuatui.com/"

browser.get(address)
sleep(0.5)


# read the data from database 
df = pd.read_csv("Output\Missing_Song_Data_2.0.csv")
def take_title(num):
    title = str(list(df.title.loc[df.index==num])[0])
    singer = str(list(df.singer.loc[df.index==num])[0])
    return title,singer


# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

df["Genre"] = None
df["Lyric"] = None
number_song = 0
total_song  = len(df.index)

while number_song <=40:
    try:
        title,singer = take_title(number_song)
        fill_input = browser.find_element_by_xpath('//*[@id="txtSearch"]')
        fill_input.send_keys(f'{title}')
        fill_input.send_keys(Keys.ENTER)
        sleep(random.randint(5,10)/10)
        print('1')
        # a loop for choosing a item in the song list
        for i in range(1,6):
            # list_song is the location of song item
            list_s = browser.find_element_by_xpath(f'/html/body/div[6]/div/div/div[1]/div[6]/ul[1]/li[{i}]/div[1]/h3/a')
            # compare both head of song item(at zing) and song(at icool)             
            if (list_s.get_attribute("title")[0] == title[0]):
             
             
                # locate the song item at zingmp3.vn   
                # list_s = browser.find_element_by_xpath(f'//*[@id="divLyric"]')
                # list_s = browser.find_element_by_xpath(f'/html/body/div[6]/div/div/div[1]/div[8]/ul[1]/li{i}/div[1]/h3/a')

                # press the right-mouse to display list /object of ActionChains
                # ActionChains(browser).click(list_song).perform
                list_s.click()
                sleep(random.randint(5,10)/10)

                #locate the genre_tag
                genre_box = browser.find_element_by_xpath('//*[@id="box_playing_id"]/div[3]/div[1]/span[2]/a')

                #add the genre to database
                df["Genre"].loc[df.index==number_song] = str(genre_box.text).replace("Bài hát ","") 
                print(genre_box.text)
                # get the song lyric
                lyrics_area = browser.find_elements_by_id('divLyric')
                lyrics = str(lyrics_area[0].text.split('\n')[1:]).replace("', '","\n")
                print(lyrics)
                # add the lyric to df
                df["Lyric"].loc[df.index==number_song] = lyrics
                break


        fill_input.clear
        number_song = number_song + 1
        print(number_song)
            
        
    except:
        fill_input.clear
        number_song = number_song + 1
        print("error ", number_song)

df.to_csv("Data/nhaccuatui_test.csv")        
# print(df.head(5))

browser.close()
browser.quit()