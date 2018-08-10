import sys
sys.path.append('../')
import of_spider
import of_utils

class EsteeLauder(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.mpp__product-grid > li > div.product_brief > a.product_brief__image-container')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h4.product-full__subtitle')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'span.product-full__price')
        if element:
            price_text = element.text.strip()[1:].strip()
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product-full__image > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.spp-product__details-description > p')
        product['detail'] = element.text.strip()
        return product