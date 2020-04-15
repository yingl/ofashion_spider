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

def getListCn(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    # prefs = {'profile.managed_default_content_settings.images': 2}
    # options.add_experimental_option('prefs',prefs)
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(15)
    try:
        btn = of_utils.find_element_by_css_selector(driver,'#addlist > a')
        if not btn:
            btn = of_utils.find_element_by_css_selector(driver,'#productGridLoadMoreLnk')

        if btn:
            driver.execute_script('arguments[0].click();', btn)
            of_utils.sleep(2)
        
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, '#pdlist a.spice-item-grid')
            if not elements:
                elements = of_utils.find_elements_by_css_selector(driver,'.product-tiles-grid article a.product-tiles-grid-item-link')

            if len(elements) > product_count:
                product_count = len(elements)
                # driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                action = ActionChains(driver).move_to_element(elements[-1])
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.perform()
                of_utils.sleep(5)
            else:
                break

        return [element.get_attribute('href').strip() for element in elements]    

    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        driver.quit()

def getDetailCn(url):
    product = of_spider.empty_product.copy()
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(15)
    try:
        product['url'] = url
        product['title'] = of_utils.find_element_by_css_selector(driver, '.spice-product-name').text.strip()
        product['code'] = of_utils.find_element_by_css_selector(driver, '.spice-style-number-title > span').text.strip()
        product['price_cny'] = of_utils.convert_price(of_utils.find_element_by_css_selector(driver, '.goods-price').text.strip())
        product['images'] = of_utils.find_element_by_css_selector(driver, '#product_main_image_0 img').get_attribute('srcset')

        return product
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        driver.quit()

def getDetail(url):
    product = of_spider.empty_product.copy()
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(15)
    try:
        product['url'] = url
        product['title'] = driver.find_element_by_xpath('//h1[contains(@class,"product-detail-product-name")]').text.strip()
        product['code'] = driver.find_element_by_xpath('//div[@class="style-number-title"]/span').text.strip()
        product['price_usd'] = of_utils.convert_price(driver.find_element_by_xpath('//input[@class="gucciProductPrice"]').get_attribute('value')) 
        product['images'] = driver.find_element_by_xpath('//img[contains(@class,"product-detail-carousel-image")][1]').get_attribute('srcset')
        return product
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        driver.quit()


def save(d):
    brandId = 3
    price = handlePrice(d)
    imgIds = []
    arr = d['images'].split(';')
    if arr:
        for a in arr:
            if a:
                imgName = ''
                image = Images(name=imgName ,url=a)
                image.save()
                imgIds.append(image.id)

    product = Products.select().where(Products.product_url==d['url'])
    if product:
        product[0].delete_instance()
    product = Products.create(name=d['title'],code=d['code'],brand_id=brandId,currency=price['currency'],price=price['price'],exrate_result=0,content=d['detail'],product_url=d['url'],status=0,buy_online=1,is_confirm=1,is_top=99,head_image_id=imgIds[0] if len(imgIds)>0 else None)
    # 保存商品图片
    if imgIds:
        for imgId in imgIds:
            Product_Images.create(product_id=product.id,image_id=imgId,status=1)

    print('%s,%s' % (product.id,product.name))

class Images(Model):
    name = TextField(default='')
    url = TextField(default='')
    width = IntegerField(default=0)
    height = IntegerField(default=0)
    ratio = TextField(default='')
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db

class Products(Model):
    name = TextField(default='')
    code = TextField(default='')
    brand_id = IntegerField()
    cate_id = IntegerField()
    currency = TextField(default='')
    price = FloatField(default=0.0)
    exrate_result = FloatField(default=0.0)
    content = TextField(default='')
    product_url = TextField(default='')
    status = IntegerField()
    created_at = DateTimeField(default=datetime.now)
    update_at = DateTimeField(default=datetime.now)
    buy_online = IntegerField(default=0)
    share_url = TextField(default='')
    is_confirm = IntegerField(default=0)
    head_image_id = IntegerField()
    is_top = IntegerField()
    class Meta:
        database = db 

class Product_Images(Model):
    product_id = IntegerField()
    image_id = IntegerField()
    image_url = TextField(default='')
    display_order = IntegerField(default=0)
    status = IntegerField(default=0)
    is_main = IntegerField(default=0)
    url = TextField(default='')
    class Meta:
        database = db

def handlePrice(obj):
    _cny = 1
    _gbp = 8.915
    _eur = 7.9543
    _jpy = 0.0612
    _usd = 6.809
    _hkd = 0.889
    currency = 'CNY'
    price = obj['price_cny']
    exrate_result = price * _cny
    return {'currency': currency,'price':price,'exrate_result':exrate_result}

def loopCn():
    url = 'https://www.gucci.cn/zh/ca/women/handbags?pn=1'
    products = getListCn(url)
    print(products)
    print(len(products))

    for p in products:
        product = getDetailCn(p)
        print(product)
        save(product)


def loop():
    url = 'https://www.gucci.com/us/en/ca/women/handbags-c-women-handbags/1'
    products = getListCn(url)
    print(products)
    print(len(products))

    for p in products:
        product = getDetail(p)
        print(product)
        save(product)


if __name__ == '__main__':
    # url = 'https://www.gucci.cn/zh/ca/women/handbags?pn=1'
    # url = 'https://www.gucci.com/us/en/ca/women/handbags-c-women-handbags/1'
    # products = getListCn(url)
    # print(products)
    # print(len(products))

    # url = 'https://www.gucci.cn/zh/pr/547947HWYAM8559?nid=12&listName=ProductGrid&position=298&categoryPath=women/handbags'
    # url = 'https://www.gucci.com/us/en/pr/women/handbags/crossbody-bags-for-women/soho-small-leather-disco-bag-p-308364A7M0G1000'
    # product = getDetail(url)
    # print(product)

    # d = {'title': 'Disney x Gucci中号托特包', 'code': '547947 HWYAM 8559', 'price_cny': 14800, 'price_euro_de': 0, 'price_euro_fr': 0, 'price_euro_ita': 0, 'price_gbp': 0, 'price_hkd': 0, 'price_jpy': 0, 'price_usd': 0, 'images': 'https://res.gucci.cn/resources/2019/12/16/15764946798382843_g_800X800.jpg', 'detail': '', 'url': 'https://www.gucci.cn/zh/pr/547947HWYAM8559?nid=12&listName=ProductGrid&position=298&categoryPath=women/handbags'}

    # save(d)


    # url1 = 'https://www.gucci.com/us/en/ca/women/handbags-c-women-handbags'
    # url2 = 'https://www.gucci.cn/zh/ca/women/handbags?pn=1'
    # loopCn()

    loop()