import sys
sys.path.append('../')
import of_spider
import of_utils

class Christofle(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, '#listItems .item>a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, "article .product_name")
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')    
        # code N/A
        # price_euro_de
        element = of_utils.find_element_by_css_selector(driver, 'article .product-price-view')
        if element:
            product['price_euro_de'] = element.get_attribute('content')
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'article #product-image-container img')
        if elements:
            images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        return product