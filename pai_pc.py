#coding:utf-8
'''UI automatic test case of shanpai-PC'''
__author__ = "yinzx"
__version__ = "1.0"

import time
import sys
import HTMLTestRunner
import unittest
from BeautifulSoup import BeautifulSoup
import re
import random
import urllib2
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException

siturl = "http://paisit.cnsuning.com/shanpai/"
items = []
html = urllib2.urlopen(siturl).read()
soup = BeautifulSoup(html)
itemlist = soup.findAll('input',id= re.compile("^itemId"))
for i in range(0,len(itemlist)):
    item = itemlist[i]['value']
    items.append(item)
print items
randitem = random.choice(items)
itemid = "itemName_i_" + randitem
print itemid
#screenshot path
imagename = "D://test//Screenshots//"+ itemid + ".png"
#login data
user = {"username":"593743227@qq.com","passwd":"1qaz2wsx"}

class PaiPcTest(unittest.TestCase):
    """docstring for PaiPcTest"""
    def setUp(self):
        self.driver = webdriver.Chrome()
        #self.driver = webdriver.Ie()
        #self.driver = webdriver.Firefox()
        self.driver.get(siturl)
        self.driver.maximize_window()
        
    def tearDown(self):
        self.driver.quit()
        
    def homepage(self):        
        js="var q= document.body.scrollTop=1000"
        #self.driver.execute_script(js)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);alert('hello!')")
        time.sleep(10)
        js= "var q= document.body.scrollTop=500"
        self.driver.execute_script(js)
        time.sleep(3)
        self.driver.find_element_by_id("2").click()     #明日预热标签
        time.sleep(2)
        self.driver.find_element_by_id("3").click()     #历史拍卖标签
        time.sleep(2)
        self.driver.find_element_by_id("4").click()     #闪拍帮助标签
        time.sleep(2)
    def test_main_process(self):
        mainwindow = self.driver.current_window_handle
        try:
            unfoldbtn = self.driver.find_element_by_name("index_allday_list_unfold")
            if unfoldbtn.is_displayed():
                unfoldbtn.click()
                time.sleep(3)
            self.driver.get_screenshot_as_file(imagename)
            self.driver.find_element_by_id(itemid).click()
            #screenshot = self.driver.get_screenshot_as_png() #binary data embedded in html
            time.sleep(3)
            allwindows = self.driver.window_handles
            for window in allwindows:
                if window!=mainwindow:
                    self.driver.switch_to_window(window)
            depbtn = self.driver.find_element_by_id("depositBtn_%s" %randitem)
            WebDriverWait(self.driver, 60).until(lambda the_driver:the_driver.find_element_by_id("depositBtn_%s" %randitem).is_displayed())
            depbtn.click()
            time.sleep(3)
            try:
                self.driver.switch_to_frame("iframeLogin")
                self.driver.find_element_by_id("loginName").clear()
                self.driver.find_element_by_id("loginName").send_keys(user["username"])
                self.driver.find_element_by_id("loginPassword").clear()
                self.driver.find_element_by_id("loginPassword").send_keys(user["passwd"])
                self.driver.find_element_by_id("loginBtn").click()
                self.driver.switch_to_window(mainwindow)
                time.sleep(3)
            except NoSuchFrameException, e:
                print "未找到登录窗口！"
        except NoSuchElementException, e:
            print u"未找到该元素！"
                     
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(PaiPcTest)
    timestr = time.strftime('%Y%m%d%H%M%S',time.localtime())
    filename = 'D://test//test_result_'+ timestr + '.html'
    print filename
    fp = open(filename,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,verbosity=1,title=u'闪拍PC测试报告',description=u'闪拍PC端基于UI的自动化测试')
    runner.run(suite)
    fp.close()

        

