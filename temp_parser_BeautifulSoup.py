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
    jobs = get_jobs(PYTHON_URL, "Python")
    for item in jobs:
        print(item)