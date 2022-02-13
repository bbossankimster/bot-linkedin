from selenium import webdriver
from settings import WEBDRIVER, WD_CACHE


def start_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument('--allow-profiles-outside-user-dir')
    options.add_argument('--enable-profile-shortcut-manager')
    options.add_argument(r'user-data-dir=' + WD_CACHE)
    #options.add_argument(r'--disk-cache-dir=null')
    options.add_argument('--profile-directory=Profile 1')
    # options.headless = True
    driver = webdriver.Chrome(WEBDRIVER, chrome_options=options)
    return driver
