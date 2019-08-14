import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class Swatch(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, '.products .product-item a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.page-title>span')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product-info-price .price')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.replace('￥','').strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.fotorama__stage__shaft>div>img')
        images =  [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        element = of_utils.find_element_by_css_selector(driver,"meta[property='og:description']")
        if element:
            product['detail'] = element.get_attribute('content').strip()
        return product