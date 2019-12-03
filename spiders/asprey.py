import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
import json

class Asprey(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        elements = of_utils.find_elements_by_css_selector(driver, ".product-item-info>a")
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, "span[data-ui-id='page-title-wrapper']")
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, ".price-wrapper .price")
        if element:
            product['price_gbp'] = element.text.strip().replace('£','')
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.fotorama__img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        return product