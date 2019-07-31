import sys
sys.path.append('../')
import of_spider
import of_utils

class Longines(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'ol.product-items > li > div > div.details > a.product-item-link')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, "meta[name=keywords]")
        if element:
            product['title'] = element.get_attribute('content').strip().split('，')[0]
        else:
            raise Exception('Title not found')    
        # code
        element = of_utils.find_element_by_css_selector(driver,"meta[property='og:title']")
        if element:
            product['code'] = element.get_attribute('content').strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product-info-price span.price')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'img.fotorama__img')
        if elements:
            images = [element.get_attribute('src').strip() for element in elements]
        else:
            elements = of_utils.find_elements_by_css_selector(driver, 'ul.newpdp-gallery-slider > li > img')
            images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        return product