import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class Adidas(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, '.product-list-grid .list-item>div>a')
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
        element = of_utils.find_element_by_css_selector(driver, '.pdp-title>h3')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver,'#itemCode')
        if element:
            product['code'] = element.get_attribute('value')
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.goods-price')
        product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.li-img img')
        images =  [element.get_attribute('data-lasysrc').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, '#description>p')
        if element:
            product['detail'] = element.text.strip()
        return product