
import parsing
from .utils import (
    send_photo,
)
from telebot import TeleBot

DEFALTKB = ['Запустить', 'Изменить входные данные']

def run(log, bot: TeleBot, tid: int|str, browser: parsing.Browser) -> None:
    browser.load_page(parsing.SINGIN_PAGE)

    send_photo(log, bot, tid, 'Скрин страницы', browser.make_full_shot())
    browser.sign_in()
    send_photo(log, bot, tid, 'Скрин страницы', browser.make_full_shot())
    browser.refresh_loop(5)

    browser.close()