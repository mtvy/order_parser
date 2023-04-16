
import parsing, time
from .utils import (
    send_photo,
    send_msg,
)
from telebot import TeleBot

DEFALTKB = ['Запустить', 'Изменить входные данные']

from random import randint
def run(log, bot: TeleBot, tid: int|str, browser: parsing.Browser) -> None:
    try:
        log.debug(f"load page: {parsing.SINGIN_PAGE}")
        browser.load_page(parsing.SINGIN_PAGE)

        log.debug(f"page screenshot")
        send_photo(log, bot, tid, 'Скрин страницы', browser.make_full_shot())
        log.debug(f"sign in")
        browser.sign_in(bot, tid, browser)
        log.debug(f"page screenshot")
        send_photo(log, bot, tid, 'Скрин страницы', browser.make_full_shot())
    
        while True:
            sl = randint(60, 120)
            time.sleep(sl)
            log.debug(f"page screenshot")
            send_photo(log, bot, tid, f'Скрин страницы до перезахода. Сон:{sl}', browser.make_full_shot())
            log.debug(f"load page: {parsing.SINGIN_PAGE}")
            browser.load_page(parsing.SINGIN_PAGE)
            log.debug(f"page screenshot")
            send_photo(log, bot, tid, f'Скрин страницы после загрузки.', browser.make_full_shot())
            log.debug(f"sign in")
            browser.sign_in(bot, tid, browser)
            log.debug(f"page screenshot")
            send_photo(log, bot, tid, f'Скрин страницы после.', browser.make_full_shot())
        
        # browser.refresh_loop(30, bot, tid)
    except Exception as err:
        send_msg(log, bot, tid, err)
        log.error(err)

    browser.close()