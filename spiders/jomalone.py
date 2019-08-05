import sys
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
sys.path.append('../')
import of_spider
import of_utils


class Jomalone(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, '.mpp_product_tile .product-link')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, ".spp_product_name")
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, ".selectBox-label")
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.split(' ')[0])
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.spp_product_image')
        if elements:
            images = [element.get_attribute('src').strip() for element in elements]
            product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver,'.spp_product_description')
        if element:
            product['detail'] = element.text.strip()
        return product
        
        