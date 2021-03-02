import undetected_chromedriver.v2 as uc
import time, conf, re, mysql.connector


def page_has_loaded():
	# fonction pour verifier chargement d'une page
	return \
		driver.execute_script('return document.readyState;') == 'complete'

# *********************
db = mysql.connector.connect(**conf.database)
cursor = db.cursor()
cursor.execute('SELECT url FROM Publication WHERE verif = 0')
data = cursor.fetchall()

#  *************************
opts = uc.ChromeOptions()
driver = uc.Chrome(options=opts)
driver.get('https://www.leboncoin.fr/')
while not page_has_loaded(): time.sleep(5)


#  *************************
try:
    time.sleep(1)
    driver.find_element_by_id('didomi-notice-agree-button').click()
    time.sleep(2)
except: pass 


# *************
for url in data:
    url = url[0]
    driver.get(url)
    while not page_has_loaded(): time.sleep(5)

    try:
        sur = driver.find_element_by_xpath('.//div[@data-qa-id="criteria_item_square"]')
        surface = sur.find_element_by_xpath('.//p[contains(text(), "Surface")]/following::p').text.split()[0]
    except Exception as err:
        print(err)
        surface = None

    try:
        pie = driver.find_element_by_xpath('.//div[@data-qa-id="criteria_item_rooms"]')
        piece = pie.find_element_by_xpath('.//p[contains(text(), "Pièces")]/following::p').text
    except Exception as err:
        print(err)
        piece = None
    
    try:
        # driver.find_element_by_xpath('.//*[@data-qa-id="adview_button_phone_contact"]').click()
        driver.find_element_by_xpath('.//div[@data-pub-id="clicknumero"]').click()
        time.sleep(1)
        tel = driver.find_element_by_xpath('div[@data-qa-id="adview_number_phone_contact"]').text
    except Exception as err:
        print(err)
        tel = None

    print(surface, piece, tel)

    break



# ***********
db.close()
# driver.close()