import undetected_chromedriver as uc
import time, conf

def page_has_loaded():
	# fonction pour verifier chargement d'une page
	return \
		chrome.execute_script('return document.readyState;') == 'complete'


driver = uc.Chrome()
driver.get('https://www.leboncoin.fr/')
# on attente la fin de la chargement de page
while page_has_loaded():
    # on attend 5s avant de re-verifier
    time.sleep(5)

# on essaye d'accepter les cookies
try:
    time.sleep(1)
    driver.find_element_by_id('didomi-notice-agree-button').click()
    time.sleep(2)
except: pass 

# on va a la page de resultat
for page in range(1, conf.PAGES)
    driver.get(f'https://www.leboncoin.fr/{conf.CATEGORIES}/{conf.TYPE}/' \
        + '' if page == 1 else f'p-{page}' )

    # un timer de 10 secondes pour chaque page
    time.sleep(10)








