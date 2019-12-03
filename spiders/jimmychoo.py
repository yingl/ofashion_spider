import sys
sys.path.append('../')
import of_spider
import of_utils

class JimmyChoo(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'ol.products>li>div>a')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(4)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        of_utils.sleep(4)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.product-information .product-name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product-information .product-price .p-price')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.product-information .product-details-image-gallery img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        element = of_utils.find_element_by_css_selector(driver,'.product-information .product-short-description')
        if element:
            product['detail'] = element.text.strip()
        return product