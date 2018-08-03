import sys
sys.path.append('../')
import of_spider
import of_utils

class Mikimoto(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product-fixed__item > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.product-info__desc')
        if element:
            element_ = of_utils.find_element_by_css_selector(element, 'h1.title')
            product['title'] = element_.text.strip()
            element_ = of_utils.find_element_by_css_selector(element, 'div.text > p')
            if element_:
                product['title'] += ' ' + element_.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'h2.h5.title')
        if element:
            product['code'] = element.text.strip()
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.owl-item > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.js-toggle-content__body > p')
        product['detail'] = element.get_attribute('innerHTML').strip()
        return product