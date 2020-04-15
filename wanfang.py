import sys
import traceback
sys.path.append('.')
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import of_spider
import of_utils
import re
import json
from datetime import datetime
from peewee import *

db = MySQLDatabase( host='rds593f78790z8p64dz1.mysql.rds.aliyuncs.com',
                    port=3306,
                    user='harry',
                    password='iss123_',
                    database='channel_chic_mini_dev',
                    charset='utf8')

def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    driver.get('http://www.wanfangdata.com.cn/searchResult/getAdvancedSearch.do?searchType=all#a_001')
    # driver.get('http://www.wanfangdata.com.cn/search/searchList.do?searchType=all&showType=&pageSize=&searchWord=%E6%96%B0%E5%9E%8B%E5%86%A0%E7%8A%B6%E7%97%85%E6%AF%92&isTriggerTag=')
    driver.implicitly_wait(15)
    driver.find_element_by_xpath("//input[@id='ddd'][1]").send_keys('新型冠状病毒')
    driver.find_element_by_xpath("//select[@name='vague_accurate'][1]/option[2]").click()
    of_utils.sleep(5)
    driver.find_element_by_xpath("//a[@id='set_advanced_search_btn']").click()
    of_utils.sleep(5)
    while True:
        eles = driver.find_elements_by_xpath("//div[@class='title']/a")
        for ele in eles:
            print(ele.text.strip())

        btnNext = driver.find_element_by_xpath("//a[@class='laypage_next']")
        if btnNext:
            btnNext.click()
            of_utils.sleep(2)
        else:
            break

    driver.quit()
    # ele = of_utils.find_element_by_css_selector(driver,'#set_advanced_search_btn')
    # driver.execute_script('arguments[0].click();', ele)
    # of_utils.sleep(5)

class Articles(Model):
    title = TextField(default='')
    type = TextField(default='')
    url = TextField(default='')
    doi = TextField(default='')
    keys = TextField(default='')
    author = TextField(default='')
    authorUnit = TextField(default='')
    journal = TextField(default='')
    journalName = TextField(default='')
    session = TextField(default='')
    category = TextField(default='')
    cateId = TextField(default='')
    publishAt = TextField(default='')
    pages = TextField(default='')
    pageNumber = TextField(default='')
    createdAt = IntegerField()
    downloadUrl = TextField(default='')
    exportUrl = TextField(default='')
    q = TextField(default='')
    rank = IntegerField()
    class Meta:
        database = db 

def detail():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    prefs = {'download.default_directory': 'E:\\file\\论文'}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    
    login(driver)
    of_utils.sleep(5)

    driver.get('http://www.wanfangdata.com.cn/details/detail.do?_type=perio&id=jths202008027#')
    driver.implicitly_wait(15)

    driver.find_element_by_xpath("//a[@id='ddownb']").click()
    
    of_utils.sleep(30)
    
    print('finish')
    
def login(driver):
    driver.get('http://my.wanfangdata.com.cn/auth/user/alllogin.do')
    driver.implicitly_wait(15)
    driver.find_element_by_xpath("//input[@id='txt_username']").send_keys('lyzy2020')
    driver.find_element_by_xpath("//input[@id='txt_password']").send_keys('tsg520')
    driver.find_element_by_xpath("//input[@id='new_sub_tj']").click()
    

if __name__ == '__main__':
    # main()
    detail()