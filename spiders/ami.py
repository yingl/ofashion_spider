import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Ami(of_spider.Spider):
    def parse_entry(self, driver):
        of_utils.sleep(5)
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_xpath(driver, '//a[@class="js-card-product-link decoration-none shopping-item__image-link lazy--fade-color"]')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(5)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//h2[@class="product-title"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver,'//div[@class="col-xs-12 mt-20"]/p[2]')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//div[@class="product-price"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.get_attribute('content'))
        # images
        elements = of_utils.find_elements_by_xpath(driver, '//img[@itemprop="image"]')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail
        element = of_utils.find_element_by_xpath(driver, '//div[@id="product_information_Advices"]')
        if element:
            product['detail'] = element.text.strip()
        return product