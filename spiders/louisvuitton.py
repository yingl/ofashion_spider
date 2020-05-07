import sys
sys.path.append('../')
import of_spider
import of_utils

class LouisVuitton(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.productItemContainer > a')
            if not elements:
                elements = of_utils.find_elements_by_css_selector(driver, 'li.productItemContainer > a')
            if not elements:
                elements = of_utils.find_elements_by_css_selector(driver, 'li.productItem > a')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(4)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]
        
    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element =  of_utils.find_element_by_xpath(driver, '//h1[@id="productName"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver, '//span[@class="sku"]')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_xpath(driver, '//div[@class="priceValue"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver, '//div[@id="productSheetSlideshow"]/div/div/ul/li/button/picture/source')
        images = [element.get_attribute('srcset').split(',')[0].replace(' 1600w','').replace(' 1280w','').replace(' 1024w','').replace(' 640w','').replace(' 480w','').replace(' 320w','').replace(' 240w','') for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail
        element = of_utils.find_element_by_xpath(driver, '//div[@id="productDescription"]')
        if element:
            product['detail'] = element.text.strip()
        return product