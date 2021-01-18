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

# login instagram
INSTAGRAM_ID = os.getenv("INSTAGRAM_ID")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get("https://www.instagram.com/accounts/login/")

WebDriverWait(browser, 3).until(
    EC.presence_of_element_located((By.CLASS_NAME, "_2hvTZ"))
)

insta_id = browser.find_element_by_name("username")
insta_password = browser.find_element_by_name("password")

insta_id.send_keys(INSTAGRAM_ID)
insta_password.send_keys(INSTAGRAM_PASSWORD)
insta_password.send_keys(Keys.ENTER)

WebDriverWait(browser, 3).until(
    EC.presence_of_element_located((By.CLASS_NAME, "qNELH"))
)

# get photos

account_name = "jinifoto"

browser.get(f"https://www.instagram.com/{account_name}")

article = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "ySN3v"))
)
hashtags = article.find_elements_by_tag_name("a")


for hashtag in hashtags:
    url = hashtag.get_attribute("href")
    # ActionChains(browser).key_down(Keys.COMMAND).key_down("t")
    browser.execute_script(
        """
        const url = arguments[0];
        window.open(`${url}`,"_blank");
        """,
        url,
    )


for window in browser.window_handles:
    browser.switch_to.window(window)
    hashtag_name = browser.find_element_by_class_name("sqdOP")
    print(hashtag_name.text)


time.sleep(3)
browser.quit()