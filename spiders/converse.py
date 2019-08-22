import sys
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
sys.path.append('../')
import of_spider
import of_utils

class Converse(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, '#sku-product-list>dl>dt>a')
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
        element = of_utils.find_element_by_css_selector(driver, '#product-name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver,'#skuCode')
        if element:
            product['code'] = element.get_attribute('value')
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '#retailPrice')
        if element:
            product['price_cny'] = of_utils.convert_price(element.get_attribute('value'))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.product-thumb-list>a>img')
        images = [element.get_attribute('src').strip().replace('S_NEW','H_NEW') for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver,'.product-description')
        if element:
            product['detail'] = element.text.strip()
        return product