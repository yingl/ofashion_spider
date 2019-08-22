import sys
sys.path.append('../')
import of_spider
import of_utils

class Pola(of_spider.Spider):
    def parse_entry(self, driver):
        urls = []
        i = 0
        elements = of_utils.find_elements_by_css_selector(driver, "#goods .product-list a") 
        for element in elements:
            urls.append('%s?%s' % (driver.current_url , i))
            i+=1     
        return urls

    def parse_product(self, driver):
        flag = int(driver.current_url.split('?')[-1])
        product = of_spider.empty_product.copy()

        #title
        element = of_utils.find_elements_by_css_selector(driver,'.product-list .name')[flag]
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_elements_by_css_selector(driver, '.product-list .value')[flag]
        if element:
             product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        images = []
        element = of_utils.find_elements_by_css_selector(driver, '.product-list .product-img img')[flag]
        if element:
            images.append(element.get_attribute('src'))
        product['images'] = ';'.join(images)
        # detail N/A
        return product