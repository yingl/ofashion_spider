import sys
sys.path.append('../')
import of_spider
import of_utils

class Kanebo(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.g-TileLinkVP__list  > li > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.g-Text > p > span.opt-fontsize--l')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny N/A
        # images
        element = of_utils.find_element_by_css_selector(driver, 'div.g-Image > p.g-Image__img > img')
        product['images'] = element.get_attribute('src').strip()
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'p.cmn-richtext > span > span.opt-fontfamily--02')
        product['detail'] = element.text.strip()
        return product