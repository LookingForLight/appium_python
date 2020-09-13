import unittest
import time
import selenium
import os
from common.HTMLTestRunner import HTMLTestRunner
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUp(self):
        print('selenium version:',selenium.__version__)
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platforVersion'] = '9'
        desired_caps['deviceName'] = 'Huawei'
        desired_caps['appPackage'] = 'com.huawei.fastapp.dev'
        desired_caps['appActivity'] = 'com.huawei.fastapp.app.management.ui.FastAppCenterActivity'
        desired_caps['noReset'] = True
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        #进入快应用首页,前提快应用加载器要先加载一个华为release包
        ele = WebDriverWait(self.driver,5,1).until(EC.presence_of_element_located((By.ID,'com.huawei.fastapp.dev:id/rl_title_icon')))
        ele.click()

    def test_a_bottom_tab_mileage(self):
        wait_element_and_click(self.driver,timeout=30,locator_by=(By.ID,'里程商城'))
        sign_ele = exist_element(self.driver,timeout=30,locator_by=(By.ID, ' 签到 '))
        take_screenshot(self.driver,'mileage')
        self.assertEqual(sign_ele,True)

    def test_b_bottom_tab_discovery(self):

        wait_element_and_click(self.driver,timeout=30,locator_by=(By.ID,'发现'))
        time.sleep(5)
        title = self.driver.find_element_by_android_uiautomator('new UiSelector().text("icon_scenery_ranking")')
        if title:
            result = True
        else:
            result = False
        take_screenshot(self.driver,'discovery')
        self.assertEqual(result,True)

    def test_c_bottom_tab_order(self):

        wait_element_and_click(self.driver,timeout=30,locator_by=(By.ID,'订单'))
        time.sleep(5)
        target_ele = self.driver.find_element_by_accessibility_id('立即登录')
        if target_ele:
            result = True
        else:
            result = False
        take_screenshot(self.driver,'order')
        self.assertEqual(result,True)

    def test_d_bottom_tab_mine(self):

        wait_element_and_click(self.driver,timeout=30,locator_by=(By.ID,'我的'))
        time.sleep(5)
        target_ele = self.driver.find_element_by_accessibility_id('登录/注册')
        if target_ele:
            result = True
        else:
            result = False
        take_screenshot(self.driver,'mine')
        self.assertEqual(result,True)

    def test_e_bottom_tab_home(self):

        wait_element_and_click(self.driver,timeout=30,locator_by=(By.ID,'首页'))
        time.sleep(5)
        huoche_ele = self.driver.find_element_by_accessibility_id('火车票')
        if huoche_ele:
            huoche_ele.click()
        target_ele = self.driver.find_element_by_accessibility_id('火车票查询')
        if target_ele:
            result = True
        else:
            result = False
        take_screenshot(self.driver,'home')
        self.assertEqual(result,True)

    @classmethod
    def tearDown(self):
        time.sleep(1)
        print('teardown ....')
        self.driver.quit()


def wait_element_and_click(driver,timeout=60,poll_frequency=0.5,locator_by=object):
    ele = WebDriverWait(driver , timeout, poll_frequency).until(EC.presence_of_element_located(locator_by))
    if ele:
        ele.click()


def exist_element(driver,timeout=60,poll_frequency=0.5,locator_by=object):
    ele = WebDriverWait(driver , timeout, poll_frequency).until(EC.presence_of_element_located(locator_by))
    if ele:
        return True
    else:
        return False

def take_screenshot(driver,name = 'takeshot'):
    """
    获取当前屏幕的截图
    :param driver:
    :param name:
    """
    day = time.strftime('%Y_%m_%d',time.localtime(time.time()))
    fq = os.getcwd()+'\\screenshot\\'+day
    tm = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
    type = '.png'
    filename= ''
    if os.path.exists(fq):
        filename = fq+"\\"+tm+"_"+name+type
    else:
        os.makedirs(fq)
        filename = fq+"\\"+tm+"_"+name+type
    driver.get_screenshot_as_file(filename)

def generate_report_url():
    """
    返回报告文件路径
    :return:
    """
    day = time.strftime('%Y_%m_%d',time.localtime(time.time()))
    fq = os.getcwd()+'\\testreport\\'+day
    tm = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
    type = '.html'
    filename= ''
    if os.path.exists(fq):
        print("11")
        filename = fq+"\\"+tm+type
    else:

        os.makedirs(fq)
        filename = fq+"\\"+tm+type
    return filename

if __name__ == "__main__":
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(MyTestCase('test_a_bottom_tab_mileage'))
    suite.addTest(MyTestCase('test_b_bottom_tab_discovery'))
    suite.addTest(MyTestCase('test_c_bottom_tab_order'))
    suite.addTest(MyTestCase('test_d_bottom_tab_mine'))
    suite.addTest(MyTestCase('test_e_bottom_tab_home'))
    file_path = generate_report_url()
    filename = open(file_path,'wb')
    runner = HTMLTestRunner(stream = filename, title= '快应用UI自动化报告', description = '首页用例')
    runner.run(suite)
    filename.close()
