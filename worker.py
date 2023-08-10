from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import random


time_pause_low = 3 # - задержка между лайками от ... сек
time_pause_up = 6 # - задержка до ... сек




#selectors:
POSTS = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[3]/article/div[1]/div/div/div' # xpath
LIKE_BUTTON = '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/div/div' # xpath
LOGIN_AREA = 'input._aa4b._add6._ac4d[name="username"]' # css
PASS_AREA = 'input._aa4b._add6._ac4d[name="password"]' # css
LOGIN_BUTTON = "button._acan._acap._acas._aj1-" # css
UNUSUAL_LOGIN = '/html/body/div[1]/section/div/div/div[3]/form' # xpath



class InstaBot:
    def __init__(self, username, password, link):
        chrome_options = Options()
        chrome_options.add_argument("--lang=en")
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        #chrome_options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.stl = []
        self.vait_time = time
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("https://www.instagram.com")
        sleep(3)
        self.enter_pass(username, password, link)


    def check_login_err(self):
        try:
            self.driver.find_element(By.XPATH, UNUSUAL_LOGIN)
            return True
        except NoSuchElementException:
            return False


    def enter_pass(self, username, password, link):
        self.driver.find_element(By.CSS_SELECTOR, LOGIN_AREA).send_keys(
            username)
        self.driver.find_element(By.CSS_SELECTOR, PASS_AREA).send_keys(
            password)
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, LOGIN_BUTTON).click()
        sleep(6)
        try:
            error = self.check_login_err()
            if error == True:
                print('Проблемы с входом в аккаунт')
                self.quit_driver()
                quit(code='')
        except Exception:
            pass

        self.driver.get(link)
        sleep(3)
        print('page ok')


    def quit_driver(self):
        self.driver.quit()


    def scrool_and_like(self):
        cntr = 0
        while True:
            #print('start scrool_and_check')
            cnt = self.find_posts_and_like(cntr)
            #print('liked for this scroll', cnt)
            if cnt == 0:
                print('No more posts to like. Stopping the bot.')
                print('all liked', cntr)
                break
            cntr += cnt
            
            time.sleep(1)
            try:
                area = self.driver.find_element(By.XPATH, POSTS).find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
            except Exception as e:
                print("not find area with posts", e)
                self.quit_driver()
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});", area)
            except Exception as e:
                print('scroll error:', e)
                break
            sleep(1)
       


    def find_posts_and_like(self, counter):
        time.sleep(1)
        #print('start find_posts_and_like')
        try:
            posts = self.driver.find_elements(By.XPATH, POSTS)
        except Exception:
            print('not find posts')
            pass

        #print(f"{len(posts)}  '- all posts len'")
        cnt_liked_post = 0
        for post in posts[counter:]:
            self.like_post(post)
            cnt_liked_post += 1
            time.sleep(random.randint(time_pause_low, time_pause_up))
        return cnt_liked_post




    def like_post(self, post):
        #print('start like_post')
        post.click()
        time.sleep(1)
        try:
            like = self.driver.find_element(By.XPATH, LIKE_BUTTON)
            ActionChains(self.driver).move_to_element(like).perform()
            like.click()
        except Exception:
            print('error with like button')
        time.sleep(1)
        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.ESCAPE)
    



def gomain(args):
    my_bot = InstaBot(args[0], args[1], args[2])
    my_bot.scrool_and_like()