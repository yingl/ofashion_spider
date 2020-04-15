import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Lesjeunesetoiles(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        urls = []
        while True:
            elements = of_utils.find_elements_by_xpath(driver, '//a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]')
            if elements:
                for ele in elements:
                    urls.append( ele.get_attribute('href').strip())

            btn = of_utils.find_element_by_xpath(driver,'//a[@class="next page-numbers"]')
            if btn:
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(5)
            else:    
                break
        return urls

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//h2[@itemprop="name"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver,'//span[@class="sku"]')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//ins//span[@class="woocommerce-Price-amount amount"][1]')
        if not element:
            element = of_utils.find_element_by_xpath(driver,'//span[@class="woocommerce-Price-amount amount"][1]')
        if element:
            product['price_euro_ita'] = int(float(element.text.replace('€','').replace(',00','').strip()))
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//img[@class="wp-post-image"]')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        element = of_utils.find_element_by_xpath(driver,'//div[@class="woocommerce-product-details__short-description"]')
        if element:
            product['detail'] = element.text.strip()
        return product