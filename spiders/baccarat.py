import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Baccarat(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_xpath(driver, '//a[@class="thumb-link reset"]')
        return [element.get_attribute('href').strip() for element in elements] 

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//h1[@class="product-name"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver,'//input[@id="pid"]')
        if element:
            product['code'] = element.get_attribute('value')
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//img[contains(@class,"primary-image")]')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        element = of_utils.find_element_by_xpath(driver,'//p[@itemprop="description"]')
        if element:
            product['detail'] = element.text.strip()
        return product