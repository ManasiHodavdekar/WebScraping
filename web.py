import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient

import time
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
browser = webdriver.Chrome(executable_path=DRIVER_BIN)
wait = WebDriverWait(browser, 10)


def create_mongo_connection():
    client = MongoClient('mongodb+srv://manasi:web_linkedin@cluster0.ebrqx.mongodb.net/webscrap?retryWrites=true&w=majority')
    return client


def push_scraped_to_mongo(data):
    client = create_mongo_connection()

    try:
       client.webscrap.linkedin_jobs.insert_many(data)
    except:
       print("Error pushing data to the db")


if __name__ == '__main__':
    browser.get("https://linkedin.com")
    username = wait.until(EC.presence_of_element_located((By.ID, 'session_key')))
    time.sleep(5)
    username.send_keys("<username>") #replace <username> with your linkedin username
    time.sleep(5)
    password = wait.until(EC.presence_of_element_located((By.ID, "session_password")))
    time.sleep(5)
    password.send_keys("<password>")  #replace <password> with your linkedin password
    time.sleep(5)
    login_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sign-in-form__submit-button")))
    login_button.click()
    time.sleep(5)
    browser.get("https://www.linkedin.com/jobs/")

    jobs = wait.until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, "job-card-square__main.relative.display-flex.flex-grow-1.flex-column.align-items-stretch")))
    
    l = []
    for job in jobs:
        d = {}
        try:
            d['job_title'] = job.find_element_by_class_name('job-card-square__title').text.split('\n')[1]
        except:
            d['job_title'] = ''
        try:
            d['company_name'] = job.find_element_by_class_name('job-card-container__company-name').text
        except:
            d['company_name'] = ''
        try:
            d['location'] = job.find_element_by_class_name('job-card-container__metadata-item').text
        except:
            d['location'] = ''
        l.append(d)
    print(l)
    push_scraped_to_mongo(l)
