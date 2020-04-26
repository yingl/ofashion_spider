import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Tagheuer(of_spider.Spider):
    def parse_entry(self, driver):
        of_utils.sleep(5)
        while True:
            btn = of_utils.find_element_by_xpath(driver,'//div[@class="show-more text-center"]/button')
            if btn:
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(5)
            else:
                break    
      
        elements = of_utils.find_elements_by_xpath(driver, '//div[@class="product"]//div[@class="image-container"]//a') 
        return [element.get_attribute('href').strip() for element in elements]  

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//h1[@class="product-name"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        element = of_utils.find_element_by_xpath(driver,'//span[@itemprop="price"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.get_attribute('content'))
        # images
        elements = of_utils.find_elements_by_xpath(driver, '//meta[@property="og:image"]')
        images = [element.get_attribute('content').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail
        element = of_utils.find_element_by_xpath(driver, '//p[@id="collapseDescription"]')
        if element:
            product['detail'] = element.text.strip()
        return product