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
import time

db = MySQLDatabase( host='rds593f78790z8p64dz1.mysql.rds.aliyuncs.com',
                    port=3306,
                    user='harry',
                    password='iss123_',
                    database='channel_chic_mini_dev',
                    charset='utf8')

def getList(q):
    url = 'https://www.ncbi.nlm.nih.gov/pubmed/?term=%s' % q
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(15)

    driver.find_element_by_xpath('//div[@id="result_action_bar"]/ul/li[3]/a').click()
    driver.find_element_by_xpath('//div[@id="display_settings_menu_ps"]/fieldset/ul/li[last()]/input').click()
    of_utils.sleep(5)
    lst = []
    while True:
        eles = driver.find_elements_by_xpath('//div[@class="rslt"]/p[@class="title"]/a')
        for e in eles:
            d = {}
            d['title'] = e.text.strip()
            d['url'] =  e.get_attribute('href')
            lst.append(d)
        # btnNext = driver.find_element_by_xpath('//a[@class="active page_link next"]')
        # if btnNext:
        #     btnNext.click()
        #     of_utils.sleep(5)
        # else:
        #     break
        break
    return lst

def getContent(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(15)
    d ={}

    eles = of_utils.find_elements_by_xpath(driver,'//div[@class="auths"]/a')
    if eles:
        auths = [e.text.strip() for e in eles]
        d['author'] = ';'.join(auths)

    ele = of_utils.find_element_by_xpath(driver,'//div[@class="rprt abstract"]/div[@class="cit"]')
    if ele:
        arr = ele.text.split('. ')
        d['journal'] = arr[0]
        d['publishAt'] = arr[1]
        d['doi'] = arr[2].replace('doi: ','')
    d['seq'] = ''    
    ele = of_utils.find_element_by_xpath(driver,'//div[@class="icons portlet"]/a')
    if not ele:
        ele = of_utils.find_element_by_xpath(driver,'//a[@ref="aid_type=doi"]')
    if ele:
        d['fullTextUrl'] = ele.get_attribute('href')
    return d
    # d['doi'] = driver.find_element_by_xpath('//a[@ref="aid_type=doi"]').text
    #author
    # d['journal'] = driver.find_element_by_xpath('//a[@alsec="jour"]').text
    #publish
    # txt = driver.find_element_by_xpath('//div[@class="rprt abstract"]/div[@class="cit"]').text
    # d['publishAt'] = txt[:txt.find('doi')].strip()
    


class Articles(Model):
    title = TextField(default='')
    journal = TextField(default='')
    doi = TextField(default='')
    seq = TextField(default='')
    author = TextField(default='')
    url = TextField(default='')
    fullTextUrl = TextField(default='')
    publishAt = TextField(default='')
    createdAt = DateTimeField(default=datetime.now)
    q = TextField(default='')
    displayOrder = IntegerField()
    status = IntegerField()
    msg = TextField(default='')
    class Meta:
        database = db 

def main():
    lst = Articles.select().where(Articles.status==0).limit(1)
    for item in lst:
        try:
            d = getContent(item.url)
            item.author = d['author']
            item.journal = d['journal']
            item.doi = d['doi']
            item.publishAt = d['publishAt']
            item.seq = d['seq']
            item.fullTextUrl = d['fullTextUrl']
            item.status = 1
            item.save()
            print('update:%s' % item.title)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            item.status = -1
            item.save()

if __name__ == '__main__':
    # q = 'SARS-COV-2'
    # lst = getList(q)
    # print(lst)
    # print(len(lst))
    # flag = 1
    # for item in lst:
    #     a =  Articles.create(title=item['title'],url=item['url'],status=0,displayOrder=flag,q=q)
    #     print('%s,%s' % (a.id,a.title))
    #     flag+=1

    # a = ' 2020 Apr 8. doi: 10.1111/1750-3841.15127. [Epub ahead of print]'
    # b = a[:a.find('doi')].strip()
    # print(b)

    url = 'https://www.ncbi.nlm.nih.gov/pubmed/32272481'
    d = getContent(url)
    print(d)