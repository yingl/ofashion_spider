import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Baumeetmercier(of_spider.Spider):
    def parse_entry(self, driver):
        of_utils.sleep(5)
        elements = of_utils.find_elements_by_xpath(driver, '//div[@class="bem-product-item__image"]/a') 
        return [element.get_attribute('href').strip() for element in elements]  

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//h1[@class="h1-title"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_xpath(driver, '//div[@class="product-gallery__col-item product-gallery__main-gallery"]//img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail
        element = of_utils.find_element_by_xpath(driver, '//div[@class="product-detail__col--item product-detail__details"]/p')
        if element:
            product['detail'] = element.text.strip()
        return product
