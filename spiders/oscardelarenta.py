import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
import json

class Oscardelarenta(of_spider.Spider):
    def parse_entry(self, driver):
        urls = []
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, '.product-img > a')
            if elements:
                for ele in elements:
                    urls.append(ele.get_attribute('href').strip())
            btn = of_utils.find_element_by_css_selector(driver,'#cphContent_ctl00_ctl02_lnkNext')
            if btn:
                driver.execute_script('arguments[0].click();', btn)
                driver.implicitly_wait(15)
            else:    
                break
        return urls

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, "#lblProductName")
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, "#cphContent_ctl02_lblPrice")
        if element:
            product['price_usd'] = int(float(element.text.strip().replace('$','').replace(',','')))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '#gal1 #owl-carousel-product-thumbs img')
        images = [element.get_attribute('src').strip().replace('/220','/1600') for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        return product