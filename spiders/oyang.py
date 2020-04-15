import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Oyang(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_xpath(driver, '//a[@class="grid-product__image-link"]')
        return [element.get_attribute('href').strip() for element in elements] 

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//h1[@class="product-single__title"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//span[@id="ProductPrice"]')
        if element:
            product['price_gbp'] = int(float(element.text.strip().replace('£','')))
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//div[@class="product-single__photo-wrapper"]/img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        return product