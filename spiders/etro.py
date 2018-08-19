import sys
sys.path.append('../')
import of_spider
import of_utils

class Etro(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'div.sn_category_products > ul > li > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.sn_product_details_aside > hgroup.sn_product_data > h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.sn_product_details_aside > hgroup.sn_product_data > h2')
        if element:
            product['code'] = element.text.strip()
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.uk-slideshow > li > a.sn_product_details_zoom > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.sn_product_description > p')
        product['detail'] = element.text.strip()
        return product