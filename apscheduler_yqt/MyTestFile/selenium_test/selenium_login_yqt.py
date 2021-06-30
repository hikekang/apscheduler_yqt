from utils.webdriverhelper import WebDriverHelper
import time
driver=WebDriverHelper.init_webdriver()
driver.get("http://yuqing.sina.com/staticweb/#/login/login")

def login_by_username(driver):
    username = driver.find_element_by_xpath("//input[@formcontrolname='userName']")
    password = driver.find_element_by_xpath("//input[@formcontrolname='password']")
    yqzcode = driver.find_element_by_xpath("//input[@formcontrolname='yqzcode']")

    submit_buttion = driver.find_element_by_xpath("//button[contains(@class,'login-form-button')]")

    username.send_keys('lsyousu')
    password.send_keys('33221100aA')
    time.sleep(15)
    submit_buttion.click()
    time.sleep(5)
    # print(driver.get_cookies())
    # print(driver.get_cookies())

# driver.add_cookie()
# driver.refresh()
def login_by_cookies(driver,cookies):
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(3)
    driver.refresh()
cookies=[{
  'domain': 'yuqing.sina.com',
  'httpOnly': True,
  'name': 'JSESSIONID',
  'path': '/',
  'secure': False,
  'value': '4BD4E374F5C7EDF6716C74AA4EE6A9E2'
}, {'domain': 'yuqing.sina.com', 'expiry': int(time.time())+604800, 'httpOnly': True, 'name': 'www', 'path': '/', 'secure': False, 'value': 'userSId_yqt365_lsyousu_827857_28087'}]
# print(int(time.time()))
login_by_cookies(driver,cookies)
