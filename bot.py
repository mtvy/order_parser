from telebot import TeleBot
from telebot.types import (
    ReplyKeyboardRemove as rmvKb,
    CallbackQuery, 
    Message, 
)
import cases, parsing
import traceback as tb, dotenv, os, logger

dotenv.load_dotenv('.env')

log = logger.newLogger(__name__, logger.DEBUG)

token = os.getenv('TOKEN')
admins = os.getenv('ADMINS')
dev = os.getenv('DEV')

log.info(f'Token:{token}')
log.info(f'Admins:{admins}')

bot = TeleBot(token)
browser = parsing.Browser(parsing.LOGIN, parsing.PASSWORD, [])

def noAccess(log, bot: TeleBot, tid: str|int) -> None:
    cases.send_msg(log, bot, tid, 'Нет доступа.', rmvKb())

menuFuncs = {
    'Запустить'              : cases.run,
    'Изменить входные данные': noAccess, 
}

@bot.message_handler(commands=['start'])
def start(msg: Message) -> None:
    tid = str(msg.chat.id)
    if tid in admins:
        log.info(f'Bot starting by user:{tid}.')
        cases.send_msg(log, bot, tid, 'Бот мониторинга', cases.get_kb(log, cases.DEFALTKB))
        return
    log.warning(f'Bot starting by user:{tid} without access.')
    noAccess(bot, tid)


@bot.message_handler(content_types=['text'])
def menu(msg: Message) -> None:
    
    tid = str(msg.chat.id)
    txt = msg.text

    if tid in admins:
        if txt in menuFuncs.keys():
            log.info(f'func:{menuFuncs[txt]} by user:{tid}.')
            menuFuncs[txt](log, bot, tid, browser)
        else:
            log.warning(f"Wrong txt:'{txt}'.")
            cases.send_msg(log, bot, tid, 'Функция не найдена!', cases.get_kb(log, cases.DEFALTKB))
    else:
        log.warning(f'Msg from user:{tid} without access.')
        noAccess(bot, tid)


@bot.callback_query_handler(func=lambda _: True)
def callback_inline(call: CallbackQuery) -> None:
    cid, uid, mid, data = (
        call.message.chat.id,
        call.from_user.id,
        call.message.message_id,
        call.data,
    )
    log.info(f"Callback call: cid:{cid} uid:{uid} mid:{mid} data:{data}")
    

if __name__ == "__main__":
    try:
        log.info('Starting...')
        bot.polling(allowed_updates="chat_member")
    except Exception as err:
        log.error(f'Get polling error.\n\n{err}\n\n{tb.format_exc()}')
