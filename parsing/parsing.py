import time

from logger import log
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

DEFAULT_LINK = "https://alma-ata.kdmid.ru/queue"
MAIN_PREF    = "orderinfo.aspx"
KP_PREF      = "CodeImage.aspx?id="
KP_PREF_LEN  = len(KP_PREF)

LOGIN    = "67641"
PASSWORD = "BFED6E7C"

def imit_browser(link: str):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=options)

    opt = webdriver.ChromeOptions()
    # opt.set_headless()
    driver = webdriver.Chrome(options=opt) 
    driver.get(link)
    pageSource = driver.page_source
    # log.info(pageSource)
    page = str(pageSource)
    kp_ind = page.find(KP_PREF) + KP_PREF_LEN
    kp_uid = page[kp_ind:kp_ind+4]
    log.warning(f'{KP_PREF}{kp_uid}')
    kaptcha_elem = driver.find_element(By.ID, "ctl00_MainContent_imgSecNum")

    log.warning(kaptcha_elem.screenshot('img.png'))

    input_field = driver.find_element(By.XPATH, "//input[@name='ctl00$MainContent$txtID']")
    input_field.send_keys(LOGIN)
    
    input_field = driver.find_element(By.XPATH, "//input[@name='ctl00$MainContent$txtUniqueID']")
    input_field.send_keys(PASSWORD)

    kaptcha = input("Введите капчу: ")

    input_field = driver.find_element(By.XPATH, "//input[@name='ctl00$MainContent$txtCode']")
    input_field.send_keys(kaptcha)

    button = driver.find_element(By.XPATH, "//input[@name='ctl00$MainContent$ButtonA']")
    
    button.click()
    
    button = driver.find_element(By.XPATH, "//input[@name='ctl00$MainContent$ButtonB']")
    button.click()

    time.sleep(4)
    driver.close()
