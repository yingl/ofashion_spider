import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class Fentybeauty(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, ".product-link") 
        return [element.get_attribute('href').strip() for element in elements]  

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '#product-content .product-name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_usd
        element = of_utils.find_element_by_css_selector(driver, '#product-content .product-price .price-sales')
        if element:
            product['price_usd'] =  int(float(element.text.strip().replace('$','')))
        # # images
        elements = of_utils.find_elements_by_css_selector(driver, '.product-primary-image .slick-list .slick-track .item a')
        if elements:
            images = [element.get_attribute('href').strip() for element in elements]
            images = {}.fromkeys(images).keys()
            product['images'] = ';'.join(images)
        # # detail N/A
        return product