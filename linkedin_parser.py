import requests
from settings import CCIE_URL, CCNP_URL, PYTHON_URL, LOGIN_URL, LINKEDIN_URL, WEBDRIVER, WD_CACHE
from bs4 import BeautifulSoup

from time import sleep
from tools.webdriver import start_chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from tools.search_result import prepare_dict, get_new_jobs


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
    result_data_list = []
    links = []
    print("name {}, date {}, location {}, title {}".format(len(company_name), len(job_date), len(job_location), len(job_title)))
    job_count = len(job_date)
    for j in range(job_count):
        a = job_date[j]
        b = company_name[j]
        c = job_location[j]
        d = job_title[j].title()
        e = job_link[j]
        result_data = {}
        result_data = {
            "job_date": a,
            "company_name": b,
            "job_location": c,
            "job_title": d,
            "job_link": e}
        if filter_title is None:
            search_result.append('{}\n{}\n{}\n{}\n'.format(d,b,a,c))
            links.append(e)
            result_data_list.append(result_data)
        else:
            if filter_title in job_title[j].title():
                search_result.append('{}\n{}\n{}\n{}\n'.format(d,b,a,c))
                links.append(e)
                result_data_list.append(result_data)
    #print(search_result[0])
    #print(links[0])
    print("pg_count", pg_count)
    return search_result, links, pg_count, result_data_list


def get_jobs(url, filter_title=None):
    print("get_jobs")
    driver = start_chrome()
    print("get_jobs")
    search_result, links, result_data_list = [], [], []
    # search_result, links, pages = parse_rqst(driver, url, filter_title)
    try:
        search_result, links, pages, result_data_list = parse_rqst(driver, url, filter_title)
    except Exception as e:
        print("Exception ERROR (parse main page)!", e)
    #driver.quit()
    print("pages")
    if pages > 1:
        # for i in range(1, pages):
        for i in range(1, 2):
            step = 25*i
            next_url = url + '&start=' + str(step)
            try:
                tmp_result, tmp_links, tmp_pages, tmp_result_data_list = parse_rqst(driver, next_url, filter_title)
            #driver.quit()
            except Exception as e:
                print("Exception error! LinkedIn page result: {}(from {})\n{}".format(i+1, pages, e))
            else:
                print("Done! LinkedIn page result: {}(from {})\n".format(i+1, pages))
                search_result = search_result + tmp_result
                links = links + tmp_links
                result_data_list = result_data_list + tmp_result_data_list
                
    res_count = len(search_result)
    summary_line = f"\n\nСкрипт выполнен.\nНайдено вакансий: {res_count}\n"
    print(summary_line)
    driver.quit()
    # sleep(160)
    raw_data = []
    return search_result, links, summary_line, result_data_list


if __name__ == "__main__1":
    jobs, links, summary_line, jobs_data_list = get_jobs(PYTHON_URL, "Python")
    fileToWrite = open("result_python_jobs.txt", "w", encoding="utf-8")
    print("\n\n>>> Final result (jobs):\n")
    for num in range(len(jobs)):
        result = f'#{num} {jobs[num]}\n'
        fileToWrite.write(result)
        print(result, end="")
    print("\n")
    print("\n\n>>> Final result (links):\n")
    for num in range(len(links)):
        result = f'#{num} {links[num]}\n'
        fileToWrite.write(result)
        print(result, end="")
    print("\n\n>>> Final result (summary_line):\n")
    print(summary_line)
    fileToWrite.write(summary_line)
    fileToWrite.close()
    prepare_dict(jobs_data_list)


if __name__ == "__main__":
    jobs_data_list = [{'job_date': 'NEW', 'company_name': 'IBM', 'job_location': 'Khabarovsk', 'job_title': 'Driver', 'job_link': 'https://www.linkedin.com/jobs/view/2856179630/'}]
    prepare_dict(jobs_data_list)
    get_new_jobs()