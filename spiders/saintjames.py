import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
import json

class SaintJames(of_spider.Spider):
    def parse_entry(self, driver):
        urls = []
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, '.product-show > a ')
            if elements:
                for ele in elements:
                    urls.append(ele.get_attribute('href').strip())
            btn = of_utils.find_element_by_css_selector(driver,'.toolbar-bottom .pager .pages .i-next')
            if btn:
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(4)
            else:    
                break
        return urls

    def parse_product(self, driver):
        of_utils.sleep(2)
        # driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, ".product-name")
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'label.regular-price>span')
        if element:
            product['price_euro_de'] = int(float(element.text.strip().replace('€','').replace(',','')))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.product-image-gallery > a > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        return product