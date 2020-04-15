import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Claudiepierlot(of_spider.Spider):
    def parse_entry(self, driver):
        driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
        btn = of_utils.find_element_by_xpath(driver,'//a[@class="pagination__all"]')
        if btn:
            driver.execute_script('arguments[0].click();', btn)
            of_utils.sleep(5)
        elements = of_utils.find_elements_by_xpath(driver, '//div[@class="product-image"]//a[@class="thumb-link"]')
        return [element.get_attribute('href').strip() for element in elements]  

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//h1[@class="productName"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//meta[@property="product:price:amount"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.get_attribute('content'))
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//div[@class="product-main-image-container"]//img[@class="img-product primary-image"]')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail
        element = of_utils.find_element_by_xpath(driver,'//meta[@property="og:description"]')
        if element:
            product['detail'] = element.get_attribute('content').strip()
        return product