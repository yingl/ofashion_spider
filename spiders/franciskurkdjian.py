import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Franciskurkdjian(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_xpath(driver, '//a[@class="product-image powerTip"]')
        return [element.get_attribute('href').strip() for element in elements]


    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//h1[@class="page-title notranslate"]/span[1]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//span[@class="current-price normal-price"]')
        if element:
            product['price_euro_ita'] = of_utils.convert_price(element.text.strip().replace('€',''))
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//img[contains(@class,"product-image")]')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        return product