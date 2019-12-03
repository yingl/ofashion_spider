import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils
import re

class Ugg(of_spider.Spider):
    def parse_entry(self, driver):
        urls = []
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, '#gallery-grid-list .product-image>a')
            if elements:
                for ele in elements:
                    urls.append(ele.get_attribute('href').strip())
            btn = of_utils.find_element_by_css_selector(driver,'.pager .next')
            if btn:
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(4)
            else:    
                break
        return urls

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '#main-info h1.product-name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, '#goodsBn')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '#main-info .product-price .goodsprice')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        images = []
        elements = of_utils.find_elements_by_css_selector(driver, '.pics-content > li > a')
        if elements:
            for ele in elements:
                imgInfo = ele.get_attribute('imginfo').strip()
                evalObj = eval(imgInfo,{'small':'small','big':'big','video':'video'})
                images.append(evalObj['big'])
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, '#main-info .description')
        if element:
            product['detail'] = element.text.strip()
        return product