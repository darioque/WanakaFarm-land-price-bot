import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import telegram_send
import schedule

def scrape():
    url = "https://marketplace.wanakafarm.com/#/lands?sale=order&sortBy=lowest-price"
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Firefox(firefox_options=options)
    driver.get(url)
    time.sleep(10) # time to wait to start scraping the html
    page = driver.page_source # raw html
    driver.quit()
    soup = BeautifulSoup(page, 'html.parser') # parsing html to text with bs4

    container = soup.find_all("span") # finding all the spans (in this case they contain a few things + all first page prices) this returns text
    id = soup.find_all('div', {'color': "#ff9800"})[1].text # finding the second div with that color (which in this case is the ID of the first item for sale)
    correct_id = id.replace("#", "") # remove its # to make it a stringed number
    return container, correct_id

def pricer(): # function to send me a message in case there's a land going for less than 500
    try:
        container, correct_id = scrape()
        print("Scraping without exceptions")
    except:
        print("There was an error while scraping")
        return
    for line in container: # line would be from <span> to </span> and line.text gets us what is inside (price in string in this case)
        if isinstance(line.text, str):
            try:
                price = int(line.text) # turn the string to a number to be able to compare (and if its not a integerable number which means it's not a price it goes to the except block)
                if price < 500:
                    with open('price.txt', 'r+', encoding="utf-8") as file: # opening in read and write without truncating
                        if file.read() == correct_id + str(price): # checking if this land has already been notified
                            return
                        file.seek(0) # To bring the pointer back to the starting of the file.
                        file.truncate() # truncating from the beginning of the file
                        file.write(correct_id + str(price)) # writing the found land
                    telegram_send.send(messages=["There is a land going for " + str(price) + "\nClick this link for the marketplace: https://marketplace.wanakafarm.com/#/lands?sale=order&sortBy=lowest-price\n" + "or click this link for the specific page: https://marketplace.wanakafarm.com/#/lands/" + correct_id])
                return
            except:
                continue

schedule.every(130).seconds.do(pricer)

while 1:
    schedule.run_pending()
    time.sleep(2)



