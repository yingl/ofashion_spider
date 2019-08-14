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
        element = of_utils.find_element_by_css_selector(driver, '.modelName.inner')
        if element:
            product['title'] = element.get_attribute('innerHTML').strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'span.item-mfc-value')
        if element:
            product['code'] = element.get_attribute('innerHTML').split(':')[-1].strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.priceUpdater > span.price > span.value')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'div.priceUpdater > div.itemPrice > span.price > span.value')
        if element:
            price_text = element.get_attribute('innerHTML').strip().replace(',', '')
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.alternativeImages > li > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.item-description-content > div > span.value')
        text = element.get_attribute('innerHTML').strip().replace('• ', '')
        product['detail'] = text
        return product