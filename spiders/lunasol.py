import sys
sys.path.append('../')
import of_spider
import of_utils

class Lunasol(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product_cat > ul.clr > li > p > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.product_summary > h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product_photo > p > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.product_summary > p.lead')
        product['detail'] = element.text.strip()
        return product