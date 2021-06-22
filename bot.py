from settings import API_KEY, USERS, CCIE_URL, CCNP_URL, PYTHON_URL
import logging
from linkedin_parser import get_jobs

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup


logging.basicConfig(
    handlers=[logging.FileHandler('bot.log', 'a', 'utf-8')],
    format='%(asctime)s %(message)s',
    # datefmt='%m-%d %H:%M',
    level=logging.INFO #CRITICAL ERROR WARNING  INFO    DEBUG    NOTSET 
)
# logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s %(message)s')

START_TEXT = """
Привет. Я парсер LinkedIn

Выберите действие:
💡 На каждом этапе можно отправить команду /open_menu для возвращения к этому меню.
"""

NEW_USER_TEST = "Привет. Я тебя не знаю. Введи команду /id"


def main():
    mybot = Updater(API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("open_menu", open_menu))
    dp.add_handler(CommandHandler("id", check_and_start))
    dp.add_handler(MessageHandler(Filters.regex('^(ccie jobs)$'), ccie))
    dp.add_handler(MessageHandler(Filters.regex('^(ccnp jobs)$'), ccnp))
    dp.add_handler(MessageHandler(Filters.regex('^(python_только в названии)$'), python_title))
    dp.add_handler(MessageHandler(Filters.regex('^(python_все)$'), python_all))
    logging.info("Бот стартовал!!!")
    mybot.start_polling()
    mybot.idle()


def user_enable(context):
    if context.user_data.get("enable"):
        return True
    else:
        return False


def check_and_start(update, context):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    if user_id in USERS:
        context.user_data["enable"] = "yes"
        check_result = f'{user_id} {user_name}, Вы в списке пользователей бота'
        update.message.reply_text(check_result, reply_markup=main_keyboard())
    else:
        check_result = f'{user_id} {user_name}, Вас нет в списке пользователей бота'
        update.message.reply_text(check_result, reply_markup=empty_keyboard())
    logging.info(check_result)


def ccie(update, context):
    if user_enable(context):
        for item in get_jobs(CCIE_URL):
            update.message.reply_text(item, reply_markup=main_keyboard())
    else:
        update.message.reply_text(NEW_USER_TEST, reply_markup=empty_keyboard())  


def ccnp(update, context):
    if user_enable(context):
        print(CCNP_URL)
        jobs = get_jobs(CCNP_URL)
        print("len ", len(jobs))
        for item in get_jobs(CCNP_URL):
            update.message.reply_text(item, reply_markup=main_keyboard())
    else:
        update.message.reply_text(NEW_USER_TEST, reply_markup=empty_keyboard())   


def python_title(update, context):
    if user_enable(context):
        for item in get_jobs(PYTHON_URL):
            if "Python" in item:
                update.message.reply_text(item, reply_markup=main_keyboard())
    else:
        update.message.reply_text(NEW_USER_TEST, reply_markup=empty_keyboard()) 


def python_all(update, context):
    if user_enable(context):
        for item in get_jobs(PYTHON_URL):
            update.message.reply_text(item, reply_markup=main_keyboard())
    else:
        update.message.reply_text(NEW_USER_TEST, reply_markup=empty_keyboard()) 


def open_menu(update, context):
    if user_enable(context):
        update.message.reply_text(START_TEXT, reply_markup=main_keyboard())
    else:
        update.message.reply_text(NEW_USER_TEST, reply_markup=empty_keyboard())


def empty_keyboard():
    return ReplyKeyboardMarkup([[]])


def main_keyboard():
    return ReplyKeyboardMarkup([['ccnp jobs'], ['ccie jobs'],["python_только в названии"], ["python_все"]])


if __name__ == "__main__":
    main()
