import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import telegram_send
import schedule
import babylon_scraper

def scrape():
    url = "https://marketplace.wanakafarm.com/#/lands?sale=order&sortBy=lowest-price"
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    time.sleep(10) # time to wait to start scraping the html
    page = driver.page_source # raw html
    driver.quit()
    soup = BeautifulSoup(page, 'html.parser') # parsing html to text with bs4
    str_price = soup.find_all("span")[26].text # finding all the spans (in this case they contain a few things + all first page prices) index 26 is supposed to be the cheapest land this returns text
    id = soup.find_all('div', {'color': "#ff9800"})[1].text # finding the second div with that color (which in this case is the ID of the first item for sale)
    correct_id = id.replace("#", "") # remove its # to make it a stringed number
    print(str_price)
    return str_price, correct_id

def wana_pricer(): # function to send me a message in case there's a land going for less than 500
    try:
        str_price, correct_id = scrape()
    except:
        return
    try:
        price = int(str_price) # turn the string to a number to be able to compare (and if its not a integerable number which means it's not a price it goes to the except block)
        if price < 500:
            with open('price.txt', 'r+', encoding="utf-8") as file: # opening in read and write without truncating
                if file.read() == str(price): # checking if this land has already been notified
                    return
                file.seek(0) # To bring the pointer back to the starting of the file.
                file.truncate() # truncating from the beginning of the file
                file.write(str(price)) # writing the found land
            telegram_send.send(messages=["There is a land going for " + str(price) + "\nClick this link for the marketplace: https://marketplace.wanakafarm.com/#/lands?sale=order&sortBy=lowest-price\n" + "or click this link for the specific page: https://marketplace.wanakafarm.com/#/lands/" + correct_id])
        return
    except:
        print("Price received from str_price wasn't an int convertible string")
        return
        
def baby_pricer():
    try:
        bnb_price, wana_price = babylon_scraper.main() # get babylon prices
    except:
        return
    if wana_price < 500 or bnb_price < 2.6:
        with open('babyprice.txt', 'r+', encoding="utf-8") as file:
            if file.read() == (str(bnb_price) + str(wana_price)): # checking if this land has already been notified
                return
            file.seek(0)
            file.truncate()
            file.write(str(bnb_price) + str(wana_price))
        telegram_send.send(messages=['There is a cheap land in babylon, check BNB and WANA' + "\nhttps://app.babylons.io/wanaka?tab=vitrine"])
    return

def main():
    baby_pricer()
    wana_pricer()

schedule.every(130).seconds.do(main)

while 1:
   schedule.run_pending()
   time.sleep(2)
