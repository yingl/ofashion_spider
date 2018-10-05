import sys
sys.path.append('../')
import of_spider
import of_utils

class Moncler(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'section.products > ul > li > div > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        of_utils.sleep(3)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.productName > span')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'span.price > span.value')
        if element:
            price_text = element.get_attribute('innerHTML').strip().replace(',', '')
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.itemImages > div.alternativeProductShots > ul > li > img')
        images = [element.get_attribute('src').strip().replace('_8_', '_14_') for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'p.EditorialDescription > span.value')
        product['detail'] = element.text.strip()
        return product