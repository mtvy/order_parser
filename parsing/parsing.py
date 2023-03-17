import requests, shutil, time, re

from logger import log
from selenium import webdriver

DEFAULT_LINK = "https://alma-ata.kdmid.ru/queue"
MAIN_PREF    = "orderinfo.aspx"
KP_PREF      = "CodeImage.aspx?id="
KP_PREF_LEN  = len(KP_PREF)

def imit_browser(link: str):
    opt = webdriver.ChromeOptions()
    # opt.set_headless()
    driver = webdriver.Chrome(options=opt) 
    driver.get(link)

def parse_image(link: str) -> bool:
    resp = requests.get(link, stream=True)
    with open('img.png', 'wb') as out_file:
        shutil.copyfileobj(resp.raw, out_file)
    log.info(f"Kaptcha ling:[{link}] PARSED")

def parse(link: str, data=None) -> str:
    resp = requests.post(link, data=data)
    page = str(resp.content)
    kp_ind = page.find(KP_PREF) + KP_PREF_LEN
    kp_uid = page[kp_ind:kp_ind+4]

    log.info(f"Get Kaptcha Link:[{DEFAULT_LINK}/{KP_PREF}{kp_uid}]")

    parse_image(f"{DEFAULT_LINK}/{KP_PREF}{kp_uid}")
