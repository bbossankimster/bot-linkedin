from settings import API_KEY, USERS, CCIE_URL, CCNP_URL, PYTHON_URL, BUTTONS, LANG
import logging
from linkedin_parser import get_jobs
import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from settings import WEBDRIVER, WD_CACHE


logging.basicConfig(
    handlers=[logging.FileHandler('bot.log', 'a', 'utf-8')],
    format='%(asctime)s %(message)s',
    # datefmt='%m-%d %H:%M',
    level=logging.INFO #CRITICAL ERROR WARNING  INFO    DEBUG    NOTSET 
)
# logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s %(message)s')

START_TEXT_RU = """
Привет. Я парсер LinkedIn

Выберите действие:
💡 На каждом этапе можно отправить команду /open_menu для возвращения к этому меню.
"""

START_TEXT_EN = """
Hi.
I can search a job by LinkedIn engine
💡 /open_menu - show main menu

Choose a keyword to start job search...
"""

if LANG == "ru":
    start_text = START_TEXT_RU
else:
    start_text = START_TEXT_EN
print(start_text)


NEW_USER_TEST = "Привет. Я тебя не знаю. Введи команду /id"


def main():
    mybot = Updater(API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("open_menu", open_menu))
    dp.add_handler(CommandHandler("id", check_and_start))
    dp.add_handler(CommandHandler("python", python_title))
    dp.add_handler(MessageHandler(Filters.regex(BUTTONS[1][1]), ccie))
    dp.add_handler(MessageHandler(Filters.regex(BUTTONS[0][1]), ccnp))
    dp.add_handler(MessageHandler(Filters.regex(BUTTONS[1][0]), ccie))
    dp.add_handler(MessageHandler(Filters.regex(BUTTONS[0][0]), ccnp))
    dp.add_handler(MessageHandler(Filters.regex(BUTTONS[2][0]), python_all))
    dp.add_handler(MessageHandler(Filters.regex(BUTTONS[2][1]), python_all))
    dp.add_handler(MessageHandler(Filters.regex(BUTTONS[3][0]), python_title))
    dp.add_handler(MessageHandler(Filters.regex(BUTTONS[3][1]), python_title))
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
        update.message.reply_text(check_result)
        update.message.reply_text(START_TEXT_EN, reply_markup=main_keyboard())    
    else:
        check_result = f'{user_id} {user_name}, Вас нет в списке пользователей бота'
        update.message.reply_text(check_result, reply_markup=empty_keyboard())
    logging.info(check_result)


def ccie(update, context):
    if user_enable(context):
        print("Поиск вакансий ccie запущен...")  
        update.message.reply_text("Поиск вакансий ccie запущен...", reply_markup=main_keyboard())      
        #jobs, links, summary_line = get_jobs(CCIE_URL)
        #write_results(jobs, links, summary_line, update)
    else:
        update.message.reply_text(NEW_USER_TEST, reply_markup=empty_keyboard())  


def ccnp(update, context):
    if user_enable(context):
        print("Поиск вакансий ccnp запущен...")  
        update.message.reply_text("Поиск вакансий ccnp запущен...", reply_markup=main_keyboard())      
        # jobs, links, summary_line = get_jobs(CCNP_URL)
        # write_results(jobs, links, summary_line, update)
    else:
        update.message.reply_text(NEW_USER_TEST, reply_markup=empty_keyboard())   


def write_results(jobs, links, summary_line, update):
        links_str = ""
        jobs_str = ""
        fileToWrite = open("__result\\result_python_jobs.txt", "a", encoding="utf-8")
        cur_time = datetime.datetime.now()
        fileToWrite.write("\n\n" + cur_time.strftime("%b %d %Y %H:%M:%S") + "\n")
        fileToWrite.write("=" * 10 + "\n")
        for num in range(len(jobs)):
            result = f'#{num} {jobs[num]}\n'
            jobs_str = jobs_str + result
        fileToWrite.write(jobs_str)
        print(jobs_str, end="")
        print("\n")
        for num in range(len(links)):
            result = f'#{num} {links[num]}\n'
            links_str = links_str + result
        fileToWrite.write(links_str)
        print(links_str, end="")
        print(summary_line)
        fileToWrite.write(summary_line)
        fileToWrite.close()
        update.message.reply_text(jobs_str, reply_markup=main_keyboard())
        update.message.reply_text(links_str, reply_markup=main_keyboard())
        update.message.reply_text(summary_line, reply_markup=main_keyboard())


def python_title(update, context):
    if user_enable(context) :
        print("Поиск вакансий Python (в названии вакансии) запущен...")  
        update.message.reply_text("Поиск вакансий Python (в названии вакансии) запущен...", reply_markup=main_keyboard())      
        jobs, links, summary_line = get_jobs(PYTHON_URL, "Python")
        write_results(jobs, links, summary_line, update)
    else:
        update.message.reply_text(NEW_USER_TEST, reply_markup=empty_keyboard()) 


def python_all(update, context):
    if user_enable(context):
        update.message.reply_text("Поиск вакансий Python ... не работает", reply_markup=main_keyboard())
    else:
        update.message.reply_text(NEW_USER_TEST, reply_markup=empty_keyboard()) 


def open_menu(update, context):
    if user_enable(context):
        update.message.reply_text(START_TEXT_EN, reply_markup=main_keyboard())
    else:
        update.message.reply_text(NEW_USER_TEST, reply_markup=empty_keyboard())


def empty_keyboard():
    return ReplyKeyboardMarkup([[]])


def main_keyboard():
    # button1
    if LANG == "ru":
        button1 = BUTTONS[0][1]
        button2 = BUTTONS[1][1]
        button3 = BUTTONS[2][1]
        button4 = BUTTONS[3][1]
    else:
        button1 = BUTTONS[0][0]
        button2 = BUTTONS[1][0]
        button3 = BUTTONS[2][0]
        button4 = BUTTONS[3][0]
    print(button4)
    return ReplyKeyboardMarkup([[button1, button2, button3], [button4]], resize_keyboard=True)




if __name__ == "__main__":
    main()
