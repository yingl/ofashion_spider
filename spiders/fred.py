import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Fred(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        while True:
            btn = of_utils.find_element_by_xpath(driver,'//div[@class="show-more"]//button')
            if btn:
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(5)
            else:    
                break

        elements = of_utils.find_elements_by_xpath(driver, '//div[@class="pdp-link"]/a')
        return [element.get_attribute('href').strip() for element in elements]  

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//h1[@class="mt-2 product-name product-title"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver,'//span[@class="product-id"]')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//div[@class="product-sidebar"]//div[@class="prices product-price"]//span')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//img[@class="zoom-popin zoom-item d-block img-fluid"]')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        element = of_utils.find_element_by_xpath(driver,'//div[@class="value content"]')
        if element:
            product['detail'] = element.text.strip()
        return product