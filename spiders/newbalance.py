import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class NewBalance(of_spider.Spider):
    def parse_entry(self, driver):
        btnShowAlls = of_utils.find_elements_by_css_selector(driver,'.page-show-all')
        if btnShowAlls:
            for btn in btnShowAlls:
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(5)
        
        elements = of_utils.find_elements_by_css_selector(driver, 'a.product-image')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        of_utils.sleep(2)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//h1[@class="product-name"][1]')
        if element:
            product['title'] = element.get_attribute('innerHTML').strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//span[@class="price"][1]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.get_attribute('innerHTML'))
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//div[@class="desktop-images Shoes"]/div/picture/img[@class="default"]')
        images = list(set([element.get_attribute('src').strip() for element in elements]))
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail
        element = of_utils.find_element_by_xpath(driver,'//div[@class="shortDesc"]')
        if element:
            product['detail'] = element.text.strip()
        return product