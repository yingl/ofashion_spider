import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Acquadiparma(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_xpath(driver, '//a[@class="product-item scroll-item fade-in f-1"]')
        return [element.get_attribute('href').strip() for element in elements]  

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//section[@class="heading"]/h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        # price_cny
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//div[contains(@class,"slide")]/img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        element = of_utils.find_element_by_xpath(driver,'//div[@class="tab-inner"]/div/p[1]')
        if element:
            product['detail'] = element.text.strip()
        return product