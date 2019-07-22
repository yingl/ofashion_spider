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
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div#productName > h1')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'div#infoProductBlock h1#productName')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.sku')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'span.sku')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'td.priceValue')
        if not element:
            element =  of_utils.find_element_by_css_selector(driver, 'div#infoProductBlock div.priceBlock div.priceValue')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.thumbnails ul li picture source')
        if not elements:
            elements = of_utils.find_elements_by_css_selector(driver, '#productMainImage source')  
        images = [element.get_attribute('srcset').strip().split(',')[0] for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.productDescription[itemprop=description]')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'div#productDescription')
        if element:
            product['detail'] = element.text.strip()
        return product