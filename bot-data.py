import undetected_chromedriver as uc
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
opts.add_experimental_option("prefs", {'protocol_handler.excluded_schemes.tel': 'false'})
driver = uc.Chrome(options=opts)
driver.maximize_window()
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
        description = driver.find_element_by_xpath('.//div[@data-qa-id="adview_description_container"]').text
    except:
        description = None

    try:
        # driver.find_element_by_xpath('.//*[@data-qa-id="adview_button_phone_contact"]').click()
        divNum = driver.find_element_by_xpath('.//div[@data-pub-id="clicknumero"]')
        btn = divNum.find_element_by_tag_name('button')
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)
        tel = driver.find_element_by_xpath('div[@data-qa-id="adview_number_phone_contact"]').text
    except Exception as err:
        print(err)
        tel = None

    print(surface, piece, tel, description)

    cursor.execute('''
        UPDATE Publication SET
        surface = %s, piece = %s, description = %s
        WHERE url = %s
    ''', (surface, piece, description, url))
    db.commit()



# ***********
db.close()
# driver.close()