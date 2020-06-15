import sys
sys.path.append('../')
import of_spider
import of_utils

class Loewe(of_spider.Spider):
    def parse_entry(self, driver):
        while True:
            btn = of_utils.find_element_by_xpath(driver,'//a[@id="capds-js-search-loadmore"]')
            if btn:
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(4)
            else:
                break    
      
        elements = of_utils.find_elements_by_xpath(driver,'//div[@class="capds-producttile swiper-container"]')
        return ['https://www.loewe.com'+element.get_attribute('data-url').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver, '//span[@id="capds-js-product-name"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        product['code'] = driver.current_url[driver.current_url.rfind('/')+1:driver.current_url.find('.html')]

        # price_cny
        element = of_utils.find_element_by_xpath(driver, '//span[@class="capds-product__price--active"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())

        # images
        elements = of_utils.find_elements_by_xpath(driver, '//div[@class="swiper-slide"]//img')
        images = [e.get_attribute('src').strip() for e in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        
        # detail
        element = of_utils.find_element_by_xpath(driver,'//div[@class="capds-product__description"]/p')
        if element:
            product['detail'] = element.text.strip()
        return product

