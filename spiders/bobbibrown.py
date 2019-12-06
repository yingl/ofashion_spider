import sys
sys.path.append('../')
import of_spider
import of_utils

class BobbiBrown(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, '.product-brief__image-link')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.product-full__title')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')

        element = of_utils.find_element_by_css_selector(driver, '.product-full__sub-line')
        if element:
            product['title'] = product['title'] + ' ' + element.text.strip()

        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product-full-price__price .price')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.product-full-image__photo--thumb')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        return product