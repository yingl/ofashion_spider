import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils
import re
import json

class Rado(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, '.watch-box > div >a')
        return [element.get_attribute('href').strip() for element in elements]  

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '#jq_hero-title')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, '.swp-specifications__watch-codes')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, "script[type='application/ld+json']")
        if element:
            productInfo = json.loads(element.get_attribute('innerHTML'))
            if productInfo:
                product['price_cny'] = productInfo['offers']['price']
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.swp-gallery__item>a')
        images = [element.get_attribute('href').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, '.swp-hero__text')
        if element:
            product['detail'] = element.text.strip()        
        return product