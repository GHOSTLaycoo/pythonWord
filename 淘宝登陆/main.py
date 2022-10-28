from selenium import webdriver
import time
from PIL import Image
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from selenium.webdriver import Chrome

from selenium.webdriver import ChromeOptions

#初始
def main():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    bro = webdriver.Chrome(options=options, executable_path='D:\\python-3.9.7\\Scripts\\chromedriver')
    bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })

    bro.maximize_window()

    bro.get("https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fi.taobao.com%2Fmy_taobao.htm%3Fnekot%3DucK8xdi8tci0%252FQ%253D%253D1663572759023")
    time.sleep(1)

    bro.find_element(By.ID, "fm-login-id").send_keys("2627233351@qq.com")
    time.sleep(1)
    bro.find_element(By.ID, "fm-login-password").send_keys("wqs199811060")
    time.sleep(1)

    GetImage(bro)

#===================================================================================

#获取
def GetImage(bro):
    # save_screenshot 就是将当前页面进行截图且保存
    bro.save_screenshot('taobao.png')

    code_img_ele = bro.find_element(By.CSS_SELECTOR, "[id='nc_1__scale_text'] > span")
    time.sleep(1)
    Action(bro, code_img_ele)

#===================================================================================

#执行
def Action(bro,code_img_ele):
    # 动作链
    action = ActionChains(bro)
    # 长按且点击
    action.click_and_hold(code_img_ele)

    # move_by_offset(x,y) x水平方向,y竖直方向
    # perform()让动作链立即执行
    action.move_by_offset(300, 0).perform()
    time.sleep(0.5)

    # 释放动作链
    action.release()
    # 登录
    bro.find_element(By.XPATH, "//*[@id='login-form']/div[4]/button").click()
    time.sleep(10)
    bro.quit() #关闭浏览器

if __name__ == "__main__":
    main()

