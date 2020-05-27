import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Etude(of_spider.Spider):
    def parse_entry(self, driver):
        of_utils.sleep(5)
        urls = []
        while True:
            btn = of_utils.find_element_by_xpath(driver, '//div[contains(@class,"etude-btn-listMore")]')
            goods_page_all =  of_utils.find_element_by_xpath(driver, '//span[contains(@class,"goods_page_all")]').text.strip()
            goods_page_now =  of_utils.find_element_by_xpath(driver, '//span[contains(@class,"goods_page_now")]').text.strip()
            if btn and goods_page_all != goods_page_now:
                driver.execute_script('arguments[0].click();', btn)
                print('click btn')
                of_utils.sleep(5)
            else:
                break    
        elements = of_utils.find_elements_by_xpath(driver,'//div[@class="product_cell_thumbBox"]') 
        for e in elements:
            urls.append('http://www.etude.cn'+e.get_attribute('onclick').strip().replace('window.open(\'','').replace('\')',''))
        return urls

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//div[@class="etude_detail_good_title select-text"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//div[contains(@class,"etude-product-detail")]//span[contains(@class,"price-new")]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//div[contains(@class,"etude_detail_abbreviations")]/a/img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail
        element = of_utils.find_element_by_xpath(driver,'//div[contains(@class,"etude_detail_good_titDesc")]')
        if element:
            product['detail'] = element.text.strip()
        return product