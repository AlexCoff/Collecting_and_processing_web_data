from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from pymongo import MongoClient
import time
from time import mktime
from datetime import datetime as dt, timedelta

firefox_options = Options()
firefox_options.add_argument('--headless')
driver = webdriver.Firefox()

class mail_reader():
    def __init__(self):
        client = MongoClient('10.0.0.85',27017)
        self.mongo_base = client['mail_db']

    def parse_page(self, letter_page):
        collection = self.mongo_base['mail.ru']

        letter = {}
        letter['from'] = letter_page.find_element_by_class_name('letter-contact').get_attribute('title')
        letter['unix_time'] = float(letter_page.find_element_by_class_name('thread__letter').get_attribute('data-id'))/10000000000
        letter['datetime'] = dt.fromtimestamp(letter['unix_time']).strftime("%m/%d/%Y, %H:%M:%S")
        letter['subject'] = letter_page.find_element_by_class_name('thread__subject').text
        letter['html'] = letter_page.find_element_by_class_name('letter__body').get_attribute('innerHTML')
        letter['text'] = letter_page.find_element_by_class_name('letter__body').text
        letter['_id'] = hash(letter['datetime']+letter['subject'])
        collection.update_one({'_id':letter['_id']},{'$set':letter},upsert=True)
    

driver.get('https://mail.ru')
elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172@mail.ru')
elem = driver.find_element_by_id('mailbox:submit').click()

elem = driver.find_element_by_id('mailbox:password')
elem.send_keys('NewPassword172')

elem.send_keys(Keys.RETURN)
time.sleep(2)

mail = driver.find_element_by_class_name('js-tooltip-direction_letter-bottom')
driver.get(mail.get_attribute('href'))

time.sleep(3)

button_panel = driver.find_elements_by_class_name('portal-menu__group_float')[1]
next_button = button_panel.find_element_by_class_name('portal-menu-element_next')

letter_reader = mail_reader()

letter = 0
while True:
    try:
        # если кнопка активна идем дальше
        time.sleep(0.4)
        next_button.find_element_by_class_name('button2_disabled')
        page = driver.find_element_by_class_name('layout__letter-content')
        letter_reader.parse_page(page)
        print(f'Прочитано письмо: {letter}')
        # выходим из цикла когда кнопка появилась
        break
    except:
        page = driver.find_element_by_class_name('layout__letter-content')
        letter_reader.parse_page(page)
        actions = ActionChains(driver)
        actions.move_to_element(next_button).click().perform()
        print(f'Прочитано письмо: {letter}')
        letter +=1

time.sleep(3)

driver.quit()# Well done