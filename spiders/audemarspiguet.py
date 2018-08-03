import sys
sys.path.append('../')
import of_spider
import of_utils

class Audemarspiguet(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'div.row > div.ewb-item[aria-hidden=false] > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'header > h1.type-header-2')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'p.watch-detail-header__reference-number')
        if element:
            product['code'] = element.text.strip().split('#')[-1]
        # price_cny N/A
        # images
        images = []
        elements = of_utils.find_elements_by_css_selector(driver, 'div.row > div.col-sm-6 > div.aspect > div > div > picture')
        for element in elements:
            text = element.get_attribute('style').strip()
            text = text.split(':')[-1].strip()
            images.append(text[5:-3])
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.watch-detail-header__description-container > div > div >p.type-body-2')
        product['detail'] = element.text.strip()
        return product