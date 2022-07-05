# import libraries
from selenium import webdriver
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_argument("--headless")

#define browser
browser = webdriver.Chrome(options = chrome_options,executable_path="D:\DS Projects\My_Crawl_Data\Main\chromedriver.exe")
browser.maximize_window()
address = "https://zingmp3.vn/tim-kiem/tat-ca?q="

browser.get(address)
sleep(1)


# read the data from database 
df = pd.read_csv("D:\DS Projects\My_Crawl_Data\Output\Missing_Song_Data_2.0.csv")

def take_title(num):
    title = str(list(df.title.loc[df.index==num]))[2:-2]
    singer = str(list(df.singer.loc[df.index==num]))[2:-2]
    return title,singer


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

df["Genre"] = None
df["Lyric"] = None
number_song = 0
total_song  = len(df.index)

while number_song <= 2000:
    try:
        title,singer = take_title(number_song)
        fill_input = browser.find_element_by_xpath('//*[@id="root"]/div[1]/header/div/div[1]/form/div/div/input')
        fill_input.send_keys(f'{title}')
        # fill_input.send_keys(f'{title} {singer}')
        fill_input.send_keys(Keys.ENTER)
        sleep(1)

        # a loop for choosing a item in the song list
        for i in range(1,6):

            # list_song is the location of song item
            list_song = browser.find_element_by_xpath(f'//*[@id="body-scroll"]/div[1]/div/div[2]/div/div[{i}]/div/div[1]/div[2]/div/span/span/span[1]/span')
            
            # compare both head of song item(at zing) and song(at icool)             
            if (list_song.text[0] == title[0]):
                # locate the song item at zingmp3.vn   
                list_s = browser.find_element_by_xpath(f'//*[@id="body-scroll"]/div[1]/div/div[2]/div/div[{i}]')
                # press the right-mouse to display list /object of ActionChains
                ActionChains(browser).context_click(list_song).perform()
                sleep(0.5)
                # identify element
                sing = browser.find_element_by_xpath('//*[@id="react-cool-portal"]/div/div/div/ul[1]/div/div[1]/div[2]/a')
                # hover over singer element
                move_to_hover = ActionChains(browser).move_to_element(sing)
                move_to_hover.perform()
                sleep(0.5)
                # identify sub menu element
                song_info_ubmenu = browser.find_elements_by_xpath('//*[@id="react-cool-portal"]/div/div/div/ul[1]/div/div[2]/div/div')
                # print(len(song_info_ubmenu))

                # get the song genre
                for item in song_info_ubmenu:
                    
                    if str(item.find_element_by_class_name("subtitle").text)[0] == "T":
                        
                        contents = item.find_element_by_class_name('content')
                        
                        df["Genre"].loc[df.index==number_song] = contents.text
                
                # get the song lyric
                lyric_button = browser.find_element_by_xpath('//*[@id="react-cool-portal"]/div/div/div/ul[2]/div/div/button[2]')
                lyric_button.click()
                sleep(0.5)
                lyrics_area = browser.find_elements_by_xpath('//*[@id="react-cool-portal"]/div[2]/div/div/div/div/div[1]/textarea')

                # add the lyric to df
                lyrics__more = lyrics_area[0].text
                lyrics = lyrics__more.split("\n")[2:]
                if "Ca" in lyrics[0]:
                    lyrics = lyrics[1:]
                # print(1)
                lyrics = str(lyrics).replace("', '", " \n ")[2:-2]
                # print((lyrics))
                df["Lyric"].loc[df.index==number_song] = lyrics
                break


        fill_input.clear()
        number_song = number_song + 1
        print(number_song)
            
        
    except:
        fill_input.clear()
        # print("error")
        number_song = number_song + 1
        print(number_song)

df.to_csv("D:\DS Projects\My_Crawl_Data\Data\mp3_0-2k.csv")        
# print(df.head(40))

browser.close()
browser.quit()

