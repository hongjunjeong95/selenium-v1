import time
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

INSTAGRAM_ID = os.getenv("INSTAGRAM_ID")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
used_photographer_name = []
max_hashtags = 15

# login instagram
class Instagraming:
    def __init__(self, url):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.url = url

    def wait_for(self, locator):
        return WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(locator)
        )

    def login(self):
        self.browser.get(f"{self.url}/accounts/login/")
        self.wait_for((By.CLASS_NAME, "_2hvTZ"))

        insta_id = self.browser.find_element_by_name("username")
        insta_password = self.browser.find_element_by_name("password")

        insta_id.send_keys(INSTAGRAM_ID)
        insta_password.send_keys(INSTAGRAM_PASSWORD)
        insta_password.send_keys(Keys.ENTER)

        self.wait_for((By.CLASS_NAME, "qNELH"))
        self.get_photos()

    def extract_data(self):
        photographer_name = self.browser.find_element_by_class_name("sqdOP")
        photographer_name = photographer_name.text

        if photographer_name:
            if photographer_name not in used_photographer_name:
                used_photographer_name.append(photographer_name)

    def get_photos(self):
        # get photos

        account_name = "jinifoto"
        self.browser.get(f"{self.url}/{account_name}")

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

        if len(used_photographer_name) < max_hashtags:
            for window in self.browser.window_handles[0:1]:
                self.browser.switch_to.window(window)
                self.browser.close()
            self.browser.switch_to.window(self.browser.window_handles[0])
            self.get_photos(self.browser.current_url)


tester = Instagraming("https://www.instagram.com")
tester.login()