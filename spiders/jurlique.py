import sys
sys.path.append('../')
import of_spider
import of_utils

class Jurlique(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product-block > div.product-img > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div > h1[itemprop=name]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.regular-price .price')
        if element:
            product['price_cny'] = of_utils.convert_price( element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '#image-gallery-zoom>div>a')
        images = [element.get_attribute('href').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.short-description > div.std[itemprop=description]')
        product['detail'] = element.text.strip()
        return product