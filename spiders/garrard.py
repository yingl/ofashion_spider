import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Garrard(of_spider.Spider):
    def parse_entry(self, driver):
        while True:
            btn = of_utils.find_element_by_xpath(driver,'//a[@class="btn btn-wide ajax-load-more"]')    
            if btn:
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(5)
            else:
                break       

        elements = of_utils.find_elements_by_xpath(driver, '//a[@class="btn product-item-button"]')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        elements = of_utils.find_elements_by_xpath(driver,'//img[@class="attachment-shop_single size-shop_single"]')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        element = of_utils.find_element_by_xpath(driver,'//p[@class="product-detail-description"]')
        if element:
            product['detail'] = element.text.strip()
        return product