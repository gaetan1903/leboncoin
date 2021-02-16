import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def page_has_loaded():
	# fonction pour verifier chargement d'une page
	return \
		chrome.execute_script('return document.readyState;') == 'complete'


def escape_cookie():
	# fonction pour echapper la demande de cookie
	chrome.get('https://www.leboncoin.fr/')
	# Attente chargement de la page
	while page_has_loaded: time.sleep(0.5)
	try:
		WebDriverWait(chrome, 5).until(EC.presence_of_element_located((By.ID, 'didomi-notice-agree-button'))).click()
	finally:
		pass



if __name__ == '__main__':
	PROXY = "socks5://127.0.0.1:9150"
	options = Options()
	options.add_argument('--proxy-server=%s' % PROXY)
	chrome = webdriver.Chrome(options=options)
	escape_cookie()