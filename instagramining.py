import time
import os
import csv

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

INSTAGRAM_ID = os.getenv("INSTAGRAM_ID")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
ACCOUNT_NAME = "jinifoto"

people_tagnames = []
max_hashtags = 15

# login instagram
class Instagraming:
    def __init__(self, url):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.url = url

    def wait_for(self, locator):
        return WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located(locator)
        )

    def save_file(self):
        file = open(f"{ACCOUNT_NAME}-report.csv", "w")
        # fieldnames = ["Account_name"]
        # writer = csv.DictWriter(file, fieldnames=fieldnames)
        # writer.writeheader()
        # for name in people_tagnames:
        #     writer.writerow(name)

        writer = csv.writer(file)
        writer.writerow(["Account_name"])

        for people_tag_name in people_tagnames:
            print(people_tag_name)
            writer.writerow((people_tag_name,))
        self.browser.quit()

    def login(self):
        self.browser.get(f"{self.url}/accounts/login/")
        self.wait_for((By.CLASS_NAME, "_2hvTZ"))

        insta_id = self.browser.find_element_by_name("username")
        insta_password = self.browser.find_element_by_name("password")

        insta_id.send_keys(INSTAGRAM_ID)
        insta_password.send_keys(INSTAGRAM_PASSWORD)
        insta_password.send_keys(Keys.ENTER)

        self.wait_for((By.CLASS_NAME, "qNELH"))
        self.get_photos(f"{self.url}/{ACCOUNT_NAME}")
        self.save_file()

    def extract_data(self):
        try:
            people_tag_name = self.browser.find_element_by_class_name("JYWcJ")
            people_tag_name = people_tag_name.get_attribute("href")

            if people_tag_name not in people_tagnames:
                people_tagnames.append(people_tag_name)
        except NoSuchElementException:
            self.browser.close()

    def get_photos(self, url):
        # get photos

        self.browser.get(url)

        article = self.wait_for((By.CLASS_NAME, "ySN3v"))
        photos = article.find_elements_by_tag_name("a")

        for photo_url in photos:
            url = photo_url.get_attribute("href")
            self.browser.execute_script(
                """
                const url = arguments[0];
                window.open(`${url}`,"_blank");
                """,
                url,
            )

        for window in self.browser.window_handles:
            self.browser.switch_to.window(window)
            self.extract_data()

        # if len(people_tagnames) < max_hashtags:
        for window in self.browser.window_handles[0:-1]:
            self.browser.switch_to.window(window)
            self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])
        # self.get_photos(self.browser.current_url)


tester = Instagraming("https://www.instagram.com")
tester.login()