import sys
sys.path.append('../')
import of_spider
import of_utils

class Balenciaga(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.products > li > article > div > a.item-link')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.modelName')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'span.item-mfc-value')
        if element:
            product['code'] = element.get_attribute('innerHTML').split(':')[-1].strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '#item-buttons-wrapper .itemPrice .value')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.alternativeImages > li > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, '.item-description-text')
        product['detail'] = element.text.strip()
        return product