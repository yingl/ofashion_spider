import sys
sys.path.append('../')
import of_spider
import of_utils

class Arcteryx(of_spider.Spider):
    def parse_entry(self, driver):
        products = []
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product-tile-inner')
        for element in elements:
            _element = of_utils.find_element_by_css_selector(element, 'a.product-tile__product-link')
            products.append(_element.get_attribute('href').strip())
        return products

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.product-name > span')
        if element:
            product['title'] = element.get_attribute('innerHTML').strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.product-price > p > span.product-price__value')
        if element:
            price_text = element.get_attribute('innerHTML').strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div#colour-thumbnails > div')
        images = [element.get_attribute('data-small-image').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.product__short-description > p')
        product['detail'] = element.get_attribute('innerHTML').strip()
        return product