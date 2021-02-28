import undetected_chromedriver as uc
import time, conf, re, mysql.connector
from datetime import datetime

# uc.TARGET_VERSION = 87
# uc.install()

def initDb():
    cursor.execute('''
        CREATE TABLE `Publication` IF NOT EXISTS (
            `url` VARCHAR(512) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
            `date_maj` DATETIME NULL DEFAULT NULL,
            `type` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `categorie` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `titre` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `prix` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `localisation` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `image` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            PRIMARY KEY (`url`) USING BTREE
        )
        COLLATE='utf8mb4_general_ci'
        ENGINE=InnoDB ;
    ''')
    db.commit()


def page_has_loaded():
	# fonction pour verifier chargement d'une page
	return \
		driver.execute_script('return document.readyState;') == 'complete'


def verifPub(a):
    ptrn = r'^https://www.leboncoin.fr/' + conf.CATEGORIES + r'/[0-9]+.htm\?ac=[0-9]+$'
    return re.match(ptrn, a.get_property('href'))


db = mysql.connector.connect(**conf.database)
cursor = db.cursor()
initDb()
exit()
options = uc.ChromeOptions()
opts = uc.ChromeOptions()
# opts.headless=True
# opts.add_argument('--headless')
# opts.add_argument(f'--proxy-server=socks5://127.0.0.1:9050')
driver = uc.Chrome(options=opts)

driver.get('https://www.leboncoin.fr/')
# on attente la fin de la chargement de page
while not page_has_loaded():
    # on attend 5s avant de re-verifier
    time.sleep(5)

# on essaye d'accepter les cookies
try:
    time.sleep(1)
    driver.find_element_by_id('didomi-notice-agree-button').click()
    time.sleep(3)
except: pass 

# on va a la page de resultat
for page in range(1, conf.PAGES):
    driver.get(f'https://www.leboncoin.fr/{conf.CATEGORIES}/{conf.TYPE}/' \
        + ('' if page == 1 else f'p-{page}') )
    while not page_has_loaded():
        # on attend 5s avant de re-verifier
        time.sleep(5)
    all_a = driver.find_elements_by_tag_name('a')
    pub = []
    for a in all_a:
        if verifPub(a):
            try:
                title = a.find_element_by_xpath('.//p[@data-qa-id="aditem_title"]')
                prix = a.find_element_by_xpath('.//span[@data-qa-id="aditem_price"]')

                # img. = a.find_element_by_tag_name('img')
                img = a.find_elements_by_xpath('.//*[contains(@src, "https://img.leboncoin.fr")]')

                prix = prix.find_element_by_tag_name('span').get_property('innerHTML')
                loc = a.find_element_by_xpath('.//div[contains(text(),"Locations")]/following::div')
                locations = loc.text
                temps = loc.find_element_by_xpath('./following::div').text
                temps = temps.split(',')
                h, m = temps[1].strip().split(':')[0], temps[1].strip().split(':')[1]
                date = datetime.now()
                if temps[0].strip() == 'Hier':
                    date = date.replace(day=date.day-1)
                date = date.replace(hour=int(h), minute=int(m), second=0)
                
                pub = {
                        'url' : a.get_property('href'),
                        'date_maj' : date,
                        'type': conf.TYPE,
                        'categorie': conf.CATEGORIES,
                        'title' : title.get_property('title'),
                        'prix' : ''.join(re.findall(r'\d', prix)),
                        'localisation': locations,
                        'image' : ','.join([im.get_property('src') for im in img])
                }

                cursor.execute('''
                    INSERT IGNORE INTO Publication VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                ''', list(pub.values()))
                db.commit()

                print(pub, end='\n\n')

                time.sleep(2)

            except Exception as err:
                print(err)
                
    
    # un timer de 10 secondes pour chaque page
    time.sleep(10)

db.close()
driver.close()








