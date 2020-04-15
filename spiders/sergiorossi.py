import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Sergiorossi(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        elements = of_utils.find_elements_by_xpath(driver, '//a[@class="pdp-link image-link"]')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//h1[@class="product-name-title"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver,'//li[@class="product-id"]')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//div[@class="primary-category-and-price"]//span[@class="sales "]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//div[@class="primary-images"]//div[@class="swiper-wrapper"]//img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        element = of_utils.find_element_by_xpath(driver,'//div[@class="info-and-care product-attributes"]/ul')
        if element:
            product['detail'] = element.text.strip()
        return product