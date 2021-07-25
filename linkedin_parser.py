import requests
from settings import CCIE_URL, CCNP_URL, PYTHON_URL, linkedin, LOGIN_URL, LINKEDIN_URL
from bs4 import BeautifulSoup

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep



def parse_rqst(driver, url, filter_title):
    #driver.implicitly_wait(10) # seconds
    links = ""
    driver.get(url)
    #driver.implicitly_wait(10)
    #sleep(60)
    #element = WebDriverWait(driver, 5)
    element = WebDriverWait(driver, 20).until(
        ec.presence_of_element_located((By.XPATH, ".//button[starts-with(@aria-label,'Page')]"))
        )
    content = driver.page_source
    fileToWrite = open("page_source.html", "w", encoding="utf-8")
    fileToWrite.write(content)
    fileToWrite.close()
    raw_data = []
    raw_data = driver.find_elements_by_xpath(".//div[@data-job-id]")
    job_content =  [i.text.split('\n') for i in raw_data]
    print("Вакансий на странице: ", len(job_content))
    job_title, company_name, job_location, job_date = [], [], [], []
    for item in job_content:
        job_title.append(item[0].title())
        company_name.append(item[1])
        job_location.append(item[2])
        if item[3] == "Top applicant" or item[3] == "Actively recruiting":
            item.pop(3)
        if "ago" in item[3]:
            job_date.append(item[3])
        else:
            job_date.append("date undefined")
    job_link_all = driver.find_elements_by_class_name('job-card-list__title')
    job_link = [i.get_attribute('href').split("?eBP")[0] for i in job_link_all]
    # starts-with(@aria-label,'Page')
    pages_count = driver.find_elements_by_xpath(".//button[starts-with(@aria-label,'Page')]")
    pg_count = int(pages_count[-1].text)
    search_result = []
    links = []
    print("name {}, date {}, location {}, title {}".format(len(company_name), len(job_date), len(job_location), len(job_title)))
    job_count = len(job_date)
    for j in range(job_count):
        a = job_date[j]
        b = company_name[j]
        c = job_location[j]
        d = job_title[j].title()
        e = job_link[j]
        if filter_title is None:
            search_result.append('{}\n{}\n{}\n{}\n'.format(d,b,a,c))
            links.append(e)
        else:
            if filter_title in job_title[j].title():
                search_result.append('{}\n{}\n{}\n{}\n'.format(d,b,a,c))
                links.append(e)
    return search_result, links, pg_count

def get_jobs(url, filter_title=None):
    options = webdriver.ChromeOptions()
    options.add_argument('--allow-profiles-outside-user-dir')
    options.add_argument('--enable-profile-shortcut-manager')
    options.add_argument(r'user-data-dir=C:\\__PYTHON')
    options.add_argument(r'--disk-cache-dir=null')
    options.add_argument('--profile-directory=Profile 1')
    driver = webdriver.Chrome("C:\\__FROM_USB_2020\\_____PY_PROJECTS\\__BOTS\\bot-linkedin\\env\\Scripts\\chromedriver.exe", chrome_options=options)
    search_result, links = [], []
    try:
        search_result, links, pages = parse_rqst(driver, url, filter_title)
    except Exception:
        print("ERROR!")
    #driver.quit()
    if pages > 1:
        for i in range(1, pages):
            step = 25*i
            next_url = url + '&start=' + str(step)
            #driver = webdriver.Chrome("C:\\__FROM_USB_2020\\_____PY_PROJECTS\\__BOTS\\bot-linkedin\\env\\Scripts\\chromedriver.exe", chrome_options=options)
            try:
                tmp_result, tmp_links, tmp_pages = parse_rqst(driver, next_url, filter_title)
            #driver.quit()
            except Exception:
                print("ERROR!")
            else:
                search_result = search_result + tmp_result
                links = links + tmp_links
                print("Поиск... Страница {} из {}".format(i+1, pages))
    res_count = len(search_result)
    summary_line = f"\n\nСкрипт выполнен.\nНайдено вакансий: {res_count}\n"
    print(summary_line)
    driver.quit()
    # sleep(160)
    fileToWrite = open("result_python_jobs.txt", "w", encoding="utf-8")
    fileToWrite.writelines(search_result)
    fileToWrite.close()
    raw_data = []
    return search_result, links, summary_line


if __name__ == "__main__":
    jobs, links, summary_line = get_jobs(PYTHON_URL, "Python")
    for num in range(len(jobs)):
        print(f'#{num} {jobs[num]}\n')
    print("\n")
    for num in range(len(links)):
        print(f'#{num} {links[num]}')
    print(summary_line)
