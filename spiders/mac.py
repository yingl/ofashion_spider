import sys
sys.path.append('../')
import of_spider
import of_utils

class Mac(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, '.product__name-link')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.product_header_name>h3')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/
        element = of_utils.find_element_by_css_selector(driver,'.product__product-details-shade-name')
        if element:
             product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product__price>span')
        if element:
            product['price_cny'] = of_utils.convert_price( element.text.strip())
        # images
        images = []
        element = of_utils.find_element_by_css_selector(driver, "meta[property='og:image']")
        if element:
            images.append(element.get_attribute('content'))
        product['images'] = ';'.join(images)
        # detail N/A
        return product
        
        