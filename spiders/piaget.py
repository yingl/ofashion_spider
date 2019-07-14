import sys
sys.path.append('../')
import of_spider
import of_utils

class Piaget(of_spider.Spider):
    def parse_entry(self, driver):
        while True:
            btn = of_utils.find_element_by_css_selector(driver,'.rcms_ctaloadmore:not(.hidden)')
            if btn:
                driver.execute_script('arguments[0].click();', btn)
                print('aa')
                of_utils.sleep(4)
            else:
                break
        elements = of_utils.find_elements_by_css_selector(driver,'.container .grid .grid__item>a')        
        return [element.get_attribute('href').strip() for element in elements]
        
    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.media__body>h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, '.product-page-ref')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product-page-price span[itemprop=price]')
        if element:
            price_text = element.text.strip() # 去掉开头的¥
            product['price_cny'] = of_utils.convert_price(price_text)
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '#product-slider .slider__body .slider__item img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, '.pdgt-')
        if element:
            product['detail'] = element.text.strip()
        return product  