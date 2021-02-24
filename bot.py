import undetected_chromedriver as uc
import time, conf, re

def page_has_loaded():
	# fonction pour verifier chargement d'une page
	return \
		driver.execute_script('return document.readyState;') == 'complete'


def verifPub(a):
    ptrn = r'^https://www.leboncoin.fr/' + conf.CATEGORIES + r'/[0-9]+.htm\?ac=[0-9]+$'
    return re.match(ptrn, a.get_property('href'))


driver = uc.Chrome()
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
        + '' if page == 1 else f'p-{page}' )
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
                prix = prix.find_element_by_tag_name('span').get_property('innerHTML')
                img = a.find_element_by_tag_name('img')
            except: pass
            
            pub.append(
                {
                    'url' : a.get_property('href'),
                    'title' : title.get_property('title'),
                    'prix' : ''.join(re.findall('\d', prix)),
                    'image' : img.get_property('src')
                }
            )
    
    # un timer de 10 secondes pour chaque page
    break
    time.sleep(10)

print(len(pub))








