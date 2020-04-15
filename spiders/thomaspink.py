import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Thomaspink(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        urls = []
        while True:
            elements = of_utils.find_elements_by_xpath(driver, '//a[@class="f-product-card__image-link"]')
            if elements:
                for ele in elements:
                    urls.append( ele.get_attribute('href').strip())

            btn = of_utils.find_element_by_xpath(driver,'//a[@rel="next"]')
            if btn:
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(5)
            else:    
                break
        return {}.fromkeys(urls).keys()

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//h1[@class="f-product-info__heading"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver,'//p[@class="f-product-info__id hidden-md-down"]')
        if element:
            product['code'] = element.text.strip().replace('ITEM: ','')
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//span[@itemprop="price"]')
        if element:
            product['price_gbp'] = int(float(element.get_attribute('content')))
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//img[@class="u-img-responsive"]')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        element = of_utils.find_element_by_xpath(driver,'//div[contains(@class,"f-tmpl-product__specs-content__section--text")]/p')
        if element:
            product['detail'] = element.text.strip()
        return product