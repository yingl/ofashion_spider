import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class Victoriabeckhambeauty(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, ".product-card-anchor") 
        return [element.get_attribute('href').strip() for element in elements]  

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.product-template__details .product-details h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product-template__details .product-details__price')
        if element:
            product['price_usd'] = int(float(element.text.strip().replace('$','')))
        # # images
        elements = of_utils.find_elements_by_css_selector(driver, '.product-image-gallery .VueCarousel-inner img')
        if elements:
            images = [element.get_attribute('src').strip() for element in elements]
            product['images'] = ';'.join(images)
        # # detail N/A
        return product