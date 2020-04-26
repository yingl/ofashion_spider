import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Makeupforever(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_xpath(driver,'//a[@class="product-name"]')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//div[@class="product-name"]/h1')
        if element:
            product['title'] = element.get_attribute('innerText').strip()
        else:
            raise Exception('Title not found')
        # code N/A
        element = of_utils.find_element_by_xpath(driver,'//div[@class="price-box"]//span[@class="price"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.get_attribute('innerText').strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver, '//img[@id="image-main"]')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail
        element = of_utils.find_element_by_xpath(driver, '//div[@class="short-description"]/div')
        if element:
            product['detail'] = element.text.strip()
        return product