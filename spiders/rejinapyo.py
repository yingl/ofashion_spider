import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class Rejinapyo(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, '.clc-Collection_Items li a')
            if len(elements) > product_count:
                product_count = len(elements)
                action = ActionChains(driver).move_to_element(elements[-1])
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.perform()
                of_utils.sleep(4)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.prd-ProductContent_Title')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.prd-ProductPrice_Price>span')
        if element:
            product['price_gbp'] = element.text.strip()[1:]
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.prd-ProductImage_Thumbs a.prd-ProductImage_Link')
        if elements:
            images =  [element.get_attribute('href').strip() for element in elements]
            product['images'] = ';'.join(images)
        else:
            elements = of_utils.find_elements_by_css_selector(driver, '.prd-ProductImage img')
            images =  [element.get_attribute('src').strip() for element in elements]
            product['images'] = ';'.join(images)
        # detail N/A
        return product