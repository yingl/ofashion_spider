import sys
import traceback
sys.path.append('.')
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import of_spider
import of_utils

class Rimowa(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_xpath(driver, '//a[@class="product-link"]')
            if len(elements) > product_count:
                product_count = len(elements)
                action = ActionChains(driver).move_to_element(elements[-1])
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.perform()
                of_utils.sleep(2)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        of_utils.sleep(2)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//h1[contains(@class,"c-product-name-pdp")]')
        if element:
            product['title'] = element.text.strip().replace('\n',' ')
        else:
            raise Exception('Title not found')
        # code N/A
        element = of_utils.find_element_by_xpath(driver,'//span[contains(@class,"o-utility")]')
        if element:
            product['code'] = element.text.strip().replace('商品编号 :','').strip()
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//div[contains(@class,"product-image-first")]/img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail
        element = of_utils.find_element_by_xpath(driver,'//p[@class="text--center c-collection-desc"]')
        if element:
            product['detail'] = element.text.strip()
        return product