import requests
from settings import CCIE_URL, CCNP_URL, linkedin, LOGIN_URL, LINKEDIN_URL
from bs4 import BeautifulSoup

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep

def get_jobs(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--allow-profiles-outside-user-dir')
    options.add_argument('--enable-profile-shortcut-manager')
    options.add_argument(r'user-data-dir=C:\\__PYTHON')
    options.add_argument('--profile-directory=Profile 1')
    driver = webdriver.Chrome("C:\\__FROM_USB_2020\\_____PY_PROJECTS\\__BOTS\\bot-linkedin\\env\\Scripts\\chromedriver.exe", chrome_options=options)

    """    driver.get("http://www.google.com")
    elem = driver.find_element_by_name("q")
    elem.send_keys("Hello WebDriver!")
    elem.submit()"""
    driver.get(url)
    sleep(3)
    # content1 = driver.find_elements_by_css_selector('.job-card-container__link job-card-container__company-name ember-view')
    company_name_all = driver.find_elements_by_class_name('job-card-container__company-name')
    company_name = [i.get_attribute('innerHTML').strip() for i in company_name_all]
    # job_date = driver.find_elements_by_css_selector('li.job-card-container__footer-item--highlighted:nth-child(1) > time:nth-child(1)')
    job_date_all = driver.find_elements_by_tag_name('time')
    job_date = [i.text for i in job_date_all if 'ago' in i.text]
    job_location_all = driver.find_elements_by_class_name('job-card-container__metadata-item')
    job_location = [i.get_attribute('innerHTML').strip() for i in job_location_all]
    job_title_all = driver.find_elements_by_class_name('job-card-list__title')
    job_title = [i.get_attribute('innerHTML').strip() for i in job_title_all] 
    job_link_all = driver.find_elements_by_class_name('job-card-list__title')
    job_link = [i.get_attribute('href').split("?eBP")[0] for i in job_link_all] 
    #link, date, company, location, position
    search_result = []
    links = ""

    for item in job_location:
        print(item)
    print("name {}, date {}, location {}, title {}".format(len(company_name), len(job_date), len(job_location), len(job_title)))
    if len(company_name) == len(job_date) == len(job_location) == len(job_title):
        job_count = len(job_date)
        for j in range(job_count):
            a = job_date[j]
            b = company_name[j]
            c = job_location[j]
            d = job_title[j].title()
            e = job_link[j]
            links = links + "\n" + e
            search_result.append('{}\n{}\n{}\n{}\n'.format(d,b,a,c))
        search_result.append(links)
        search_result.append(f"Найдено вакансий: {job_count}\n")
    else:
        search_result.append("Ошибка в парсинге\n")
        print("Ошибка в парсинге")
        search_result.append("name {}, date {}, location {}, title {}".format(len(company_name), len(job_date), len(job_location), len(job_title)))
    # sleep(160)
    print("Close")
    driver.close
    return search_result


def login():
    client = requests.Session()
    html = client.get(HOMEPAGE_URL).content
    soup = BeautifulSoup(html, "html.parser")
    # csrf = soup.find(id="loginCsrfParam-login")['value']
    linkedin.update(loginCsrfParam="e2458b5a-dcf5-4999-8000-250ca7e56230")
    print(linkedin)
    client.post(LOGIN_URL, data=linkedin)
    html = client.get(CCNP).content
    soup = BeautifulSoup(html, "html.parser")
    result = soup.findAll(
                lambda tag:tag.name == "a" and
                len(tag["class"]) == 1)
    for item in result:
        pass
        print(item.text)



def get_jobs_bs(url):
    client = requests.Session()
    html = client.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    search_result = []
    srch_date = {}

    #link, date, company, location, position
    # date
    for JobPostings in soup.find_all('time'):
        srch_date.update(date = JobPostings.text.strip())
        search_result.append(srch_date)
        #print(search_result)
        srch_date = {}
    # company
    print(search_result)
    print(len(search_result))

    i = 0
    # job-card-container__link job-card-container__company-name ember-view

    #('a', attrs={'class' :"job-card-container__link job-card-container__company-name"})
    for JobPostings in soup.find_all('a', attrs={'class': 'hidden-nested-link'}):
        search_result[i].update(company=JobPostings.text.strip())
        i += 1

    """result = soup.findAll(
                lambda tag:tag.name == "a" and
                len(tag["class"]) == 1)
    for item in result:
        pass
        print(item.text) """           
    #print(result.text)
    # location
    for JobPostings in soup.find_all('span', attrs={'class' : 'job-search-card__location'}):
        search_result[i]['location'] = JobPostings.text.replace(", Tel Aviv, Israel", "").replace("Central, Israel","Central").replace("Israel", "").strip()
        i += 1
    # url
    for JobPostings in soup.find_all('span', attrs={'class' : 'screen-reader-text'}):
        #print(JobPostings.text, i)
        search_result[i].update(position=JobPostings.text.strip())
        print(search_result[i])
        i += 1    
    # position
    i = 0
    for JobPostings in soup.find_all('span', attrs={'class' : 'screen-reader-text'}):
        #print(JobPostings.text, i)
        search_result[i].update(position=JobPostings.text.strip())
        print(search_result[i])
        i += 1
    # link, date, company, location, position
    search_res = []
    for j in range(len(search_result)):
        a = search_result[j]['date']
        b = search_result[j]['company']
        c = search_result[j]['location']
        d = search_result[j]['position'].replace("Radware","Radware      ")
        company_n = b.upper() + " " + c
        search_res.append('{}\n{}\n{} ____ {}\n'.format(d,b,a,c))
    search_res.append(f"Найдено вакансий: {len(search_result)}\n")
    for item in search_res:
        print(item)
    return search_res

if __name__ == "__main__":
    jobs = get_jobs(CCIE_URL)
    print(len(jobs))