import sys
sys.path.append('../')
import of_spider
import of_utils

class GiuseppeZanotti(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product > div.inner > figure > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'head > title')
        if element:
            product['title'] = element.get_attribute('innerHTML').split('|')[0].strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'footer > p')
        if element:
            product['code'] = element.text.split(' ')[1].strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.prices > span.price > span > span.price')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'div.prices > span.price > p.old-price > span')
        if element:
            price_text = element.get_attribute('innerHTML')
            price_text = price_text.split(';')[1].strip().replace(',', '')
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.images > li > a')
        images = [element.get_attribute('data-zoom-image').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        return product