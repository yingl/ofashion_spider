import sys
sys.path.append('../')
import of_spider
import of_utils

class DeBeers(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        elements = of_utils.find_elements_by_xpath(driver,'//div[@class="h-100 position-relative product-tile"]/a')    
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver, '//div[@id="productInfoDiv"]//span[@class="dbj-font-header2"]')
        if element:
            product['title'] = element.get_attribute('innerHTML')
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver, '//p[@class="dbj-font-caption1-alt1 pb-1 dbj-border-top"]/span')
        if element:
            product['code'] = element.get_attribute('innerHTML').replace('&nbsp;','')
        # price_cny
        element = of_utils.find_element_by_xpath(driver, '//div[@id="productInfoDiv"]//span[@class="dbj-font-header6 product-price"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.get_attribute('innerHTML'))
        # images
        elements = of_utils.find_elements_by_xpath(driver, '//div[@class="zoom-trap"]/img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_xpath(driver, '//div[@id="pdpDesktopSlot1"]//p[@class="dbj-font-body1"]')
        if element:
            product['detail'] = element.text.strip()
        return product