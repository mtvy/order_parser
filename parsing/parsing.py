import time

from logger import log
from selenium import webdriver
from selenium.webdriver.common.by import By

from .decoder import decodeCaptcha

DEFAULT_LINK = "https://alma-ata.kdmid.ru/queue"
MAIN_PREF    = "orderinfo.aspx"
KP_PREF      = "CodeImage.aspx?id="
KP_PREF_LEN  = len(KP_PREF)

LOGIN    = "67641"
PASSWORD = "BFED6E7C"

def imit_browser(link: str):
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(10)

    driver.get(link)
    time.sleep(10)
    pageSource = driver.page_source
    page = str(pageSource)
    kp_ind = page.find(KP_PREF) + KP_PREF_LEN
    kp_uid = page[kp_ind:kp_ind+4]
    log.warning(f'{KP_PREF}{kp_uid}')
    captcha_elem = driver.find_element(By.ID, "ctl00_MainContent_imgSecNum")

    log.warning(captcha_elem.screenshot('img.png'))

    with open('img.png', 'rb') as f:
        imgb = f.read()

    captcha = decodeCaptcha(imgb)
    
    log.warning(captcha)

    input_field = driver.find_element(By.XPATH, "//input[@name='ctl00$MainContent$txtID']")
    input_field.send_keys(LOGIN)
    
    input_field = driver.find_element(By.XPATH, "//input[@name='ctl00$MainContent$txtUniqueID']")
    input_field.send_keys(PASSWORD)
    
    time.sleep(10)
    input_field = driver.find_element(By.XPATH, "//input[@name='ctl00$MainContent$txtCode']")
    input_field.send_keys(captcha)

    time.sleep(1)
    button = driver.find_element(By.XPATH, "//input[@name='ctl00$MainContent$ButtonA']")
    
    button.click()
    time.sleep(10)
    
    button = driver.find_element(By.XPATH, "//input[@name='ctl00$MainContent$ButtonB']")
    button.click()

    time.sleep(40)
    driver.close()
