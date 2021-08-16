from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os

# you'll need to provide your own link to the job search results from LinkedIn
LINK = "https://www.linkedin.com/jobs/search/?f_AL=true&f_WRA=true&geoId=104769905&keywords=counsel&location=Sydney%2C%20New%20South%20Wales%2C%20Australia"
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER")

chrome_driver_path = "C:\Program Files\Development\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get(LINK)
time.sleep(15)

login_page = driver.find_element_by_class_name("nav__button-secondary")
login_page.click()
time.sleep(15)

email_field = driver.find_element_by_id("username")
email_field.send_keys(EMAIL)

password_field = driver.find_element_by_id("password")
password_field.send_keys(PASSWORD)
time.sleep(5)

password_field.send_keys(Keys.ENTER)

#
job_search_results = driver.find_elements_by_css_selector(".job-card-container--clickable")

for job_posting in job_search_results:
    job_posting.click()
    time.sleep(5)

    try:
        apply = driver.find_element_by_css_selector(".jobs-s-apply button")
        apply.click()
        time.sleep(15)

        phone = driver.find_element_by_class_name("fb-single-line-text__input")
        if phone.text == "":
            phone.send_keys(PHONE_NUMBER)

        submit = driver.find_element_by_css_selector("footer button")

        if submit.get_attribute("data-control-name") == "continue-unify":
            close = driver.find_element_by_class_name("artdeco-modal__dismiss")
            close.click()
            time.sleep(5)

            discard = driver.find_elements_by_class_name("artdeco-modal__confirm-dialog-btn")[1]
            discard.click()
            print("Complex application, skipped.")
            continue

        else:
            submit.click()

        close = driver.find_element_by_class_name("artdeco-modal__dismiss")
        close.click()

    except NoSuchElementException:
        print("No application button, skipped.")
        continue


driver.quit()
