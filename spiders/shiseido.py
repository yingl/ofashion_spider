import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Shiseido(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_xpath(driver, '//a[@class="thumb-link"]')
        return [element.get_attribute('href').strip() for element in elements]  

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//div[@class="product-title "]/h2[@class="product-name"][1]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//div[@class="price-row"]//h2[@class="price-sales"][1]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//li[contains(@class,"productthumbnail")]/img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        element = of_utils.find_element_by_xpath(driver,'//div[@class="pdp-tab-content"]/p')
        if element:
            product['detail'] = element.text.strip()
        return product