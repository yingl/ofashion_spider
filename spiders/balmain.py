import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class Balmain(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, "ul.products li div.product_image a") 
        return [element.get_attribute('href').strip() for element in elements]  

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.item_name>span>span')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny N/A
        elements = of_utils.find_elements_by_css_selector(driver, '.mainImage img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # # detail
        element = of_utils.find_element_by_css_selector(driver, '#accordionBody_item_sizeFit')
        product['detail'] = element.text.strip()
        return product