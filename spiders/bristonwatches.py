import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
import json

class BristonWatches(of_spider.Spider):
    def parse_entry(self, driver):
        urls = []
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, '.product-image-link')
            if elements:
                for ele in elements:
                    urls.append(ele.get_attribute('href').strip())
            btn = of_utils.find_element_by_css_selector(driver,'ul.page-numbers .next')
            if btn:
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(4)
            else:    
                break
        return urls

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, ".product_title")
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, ".product-image-summary .woocommerce-Price-amount")
        if element:
            product['price_euro_de'] = int(float(element.text.strip().replace('€','').replace(',','')))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.product-image-wrap > figure > a > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        return product