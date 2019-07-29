import sys
sys.path.append('../')
import of_spider
import of_utils

class Lorealparis(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, '.product-list ul li a')
        return [element.get_attribute('href').strip() for element in elements if 'tmall' not in element.get_attribute('href').strip()]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.product-info-h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product-info .price')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip().replace('ml',''))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.product-pic .item img')
        if not elements:
            elements = of_utils.find_elements_by_css_selector(driver,'.productpage-images .productpage-image img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, '.tab-product-info')
        if element:
            product['detail'] = element.text.strip()
        return product