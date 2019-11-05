import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
import json

class Loropiana(of_spider.Spider):
    def parse_entry(self, driver):
        urls = []
        elements = of_utils.find_elements_by_css_selector(driver, ".js-gtm-product-click")
        if elements:
            for ele in elements:
                str1 = ele.get_attribute('data-gtm-info')
                info = json.loads(str1)
                urls.append('https://cn.loropiana.com/zh' + info['url'])
        return urls

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.product-info .t-h2')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # subtitle
        element = of_utils.find_element_by_css_selector(driver, '.product-info .t-sub-h3')
        if element:
            product['title'] = product['title'] + ' ' + element.text.strip()
        # code N/A
        element = of_utils.find_element_by_css_selector(driver, '.product-info .t-product-copy')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product-info .t-product-cta-price')
        if element:
            product['price_cny'] =  of_utils.convert_price(element.text)
        # # images
        elements = of_utils.find_elements_by_css_selector(driver, '.files img')
        if elements:
            images = [element.get_attribute('src').strip() for element in elements]
            product['images'] = ';'.join(images)
        # # detail N/A
        element = of_utils.find_element_by_css_selector(driver,'.product-info .t-caption')
        if element:
            product['detail'] = element.text.strip()
        return product