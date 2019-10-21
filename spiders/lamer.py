import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class Lamer(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, ".product-brief__extras-link") 
        return [element.get_attribute('href').strip() for element in elements]  

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.product-full__subline')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product-full__content .product-sku-price__value')
        if element:
            product['price_cny'] =  of_utils.convert_price(element.text.strip())
        # # images
        elements = of_utils.find_elements_by_css_selector(driver, '.product-full__image-carousel .product-full__carousel__slides .product-full__carousel__slide img')
        images = ['https://www.lamer.com.cn'+element.get_attribute('data-src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # # detail
        element = of_utils.find_element_by_css_selector(driver, '.product-full__description .product-full__accordion__panel')
        if element:
            product['detail'] = element.text.strip()
        return product
