import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Ports(of_spider.Spider):
    def parse_entry(self, driver):
        urls = []
        while True:
            elements = of_utils.find_elements_by_xpath(driver,'//div[@class="prod_list"]//div[@class="pic_main"]/a')
            if elements:
                for e in elements:
                    urls.append(e.get_attribute('href').strip())

            btn = of_utils.find_element_by_xpath(driver,'//ul[@class="pagination"]//a[@class="next"]')       
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
        element = of_utils.find_element_by_xpath(driver,'//div[@class="prod_detzone_info"]/h3')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver,'//div[@class="prod_detzone_info"]/div[@class="dec"]')
        if element:
            product['code'] = element.text.strip().replace('款号：','')
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//div[@class="prod_detzone_info"]/h4')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//div[@class="pic_all texiao"]/div')
        images = [element.get_attribute('data-bigimg').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        element = of_utils.find_element_by_xpath(driver,'//div[@class="note"]/small[1]')
        if element:
            product['detail'] = element.text.strip()
        return product