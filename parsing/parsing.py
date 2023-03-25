import time, base64

from logger import log
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from typing import List

from .decoder import decodeCaptcha

DEFAULT_LINK = "https://alma-ata.kdmid.ru/queue"
MAIN_PREF    = "orderinfo.aspx"
KP_PREF      = "CodeImage.aspx?id="
KP_PREF_LEN  = len(KP_PREF)

SINGIN_PAGE = f"{DEFAULT_LINK}/{MAIN_PREF}"

LOGIN    = "67641"
PASSWORD = "BFED6E7C"

class Browser:

    def __init__(self, login: str, password: str, opts: List[str]=[]) -> None:
        self.set_opt(opts)
        self.set_driver()
        self.login = login
        self.password = password
        self.refresh_count = 0
        self.hash = self.__hash__()
    
    def set_driver(self) -> None:
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.driver.implicitly_wait(10)
        log.info("Setuped new Chrome driver")
    
    def set_opt(self, opts: List[str]) -> None:
        """
        Default opt:
            '--no-sandbox'
            '--headless'
            '--disable-gpu'
        """
        self.chrome_options = webdriver.ChromeOptions()
        for opt in opts:
            self.chrome_options.add_argument(opt)
        log.info(f"Setuped opts:[{opts}]")
    
    def load_page(self, link: str) -> None:
        self.driver.get(link)
        log.info(f"Got page:'{link}'")

    def find_elem(self, elem: str, find_cond: str) -> WebElement:
        try:
            web_elem = self.driver.find_element(find_cond, elem)
            log.info(f"Got web_elem:'{elem}'")
            return web_elem
        except Exception as err:
            log.error(f"find_elem error:'{err}'")
            return

    def make_recap(self, elem: WebElement) -> str:
        recap = ''
        try:
            recap = decodeCaptcha(self.make_shot(elem))
            log.info(f"Got recap:'{recap}'")
        except Exception as err:
            log.error(f"decodeCaptcha error:'{err}'")
        return recap
    
    def sign_in(self) -> bool:

        cap = self.find_elem("ctl00_MainContent_imgSecNum", By.ID)
        recap = self.make_recap(cap)

        if not recap:
            log.error("Wrong captcha decode!")
            return False
        
        self.find_elem(
            "//input[@name='ctl00$MainContent$txtID']", 
            By.XPATH,
        ).send_keys(self.login)
    
        self.find_elem(
            "//input[@name='ctl00$MainContent$txtUniqueID']", 
            By.XPATH,
        ).send_keys(self.password)
    
        self.find_elem(
            "//input[@name='ctl00$MainContent$txtCode']",
            By.XPATH,
        ).send_keys(recap)

        time.sleep(3)
        self.find_elem(
            "//input[@name='ctl00$MainContent$ButtonA']", 
            By.XPATH,
        ).click()

        time.sleep(3)
        self.find_elem(
            "//input[@name='ctl00$MainContent$ButtonB']",
            By.XPATH, 
        ).click()

        return True
    
    def close(self) -> None:
        self.driver.close()
        log.info(f"Browser:'{self.hash}' closed")

    def refresh(self) -> None:
        self.driver.refresh()
        self.refresh_count += 1
        log.debug(f"Page refreshed:{self.refresh_count}")

    def sleep_day_parts(self, count_parts: int) -> None:
        day_seconds = 24 * 60 * 60
        part = day_seconds // count_parts
        log.debug(f"Sleeper start for {part} seconds")
        time.sleep(part)
        log.debug(f"Sleeper sleeped for {part} seconds")
    
    def refresh_loop(self, day_click_count: int) -> None:
        max_count = self.refresh_count + day_click_count
        log.info(f"Refresh loop started. "
                 f"refreshes:{self.refresh_count} "
                 f"stop_count:{max_count}")
        while self.refresh_count < max_count:
            self.refresh()
            # TODO: ACTION
            self.sleep_day_parts(day_click_count)

    def make_shot(self, elem: WebElement) -> bytes:
        log.info(f"Make shot")
        return elem.screenshot_as_png
        
    def make_full_shot(self) -> bytes:
        log.info(f"Make full shot")
        return self.driver.get_screenshot_as_png()

def imit_browser(link: str):
    browser = Browser(LOGIN, PASSWORD, [])
    browser.load_page(link)

    browser.sign_in()
    browser.refresh_loop(5)

    browser.close()
