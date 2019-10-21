import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
import re

class Clinique(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, '#mpp-product-grid .mpp-product>a:not(.btn-quickview)')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, ".container h1")
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')    
        # code
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.container .col2 .price .formatted_price')
        if element:
            arr = re.findall(r"¥(.*)",element.text.strip())
            if arr:
                product['price_cny'] = of_utils.convert_price(arr[0])
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.product-img')
        if elements:
            images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        element = of_utils.find_element_by_css_selector(driver,".abstract")
        if element:
            product['detail'] = element.text.strip()
        return product