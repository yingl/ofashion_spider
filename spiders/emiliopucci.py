import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class Emiliopucci(of_spider.Spider):
    def parse_entry(self, driver):
        of_utils.sleep(4)
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, '#siteContent ul li a')
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
        element = of_utils.find_element_by_css_selector(driver, 'meta[property="og:title"]')
        if element:
            product['title'] = element.get_attribute('content')
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'meta[property="product:price:amount"]')
        if element:
            product['price_cny'] =  element.get_attribute('content')
        # # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div[data-test="product-imagesContainer"] img')
        if elements:
            images = [element.get_attribute('src').strip() for element in elements]
            product['images'] = ';'.join(images)
        # # detail N/A
        return product