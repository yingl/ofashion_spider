import sys
sys.path.append('../')
import of_spider
import of_utils

class Fancl(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'ul > li > div > a.fancybox')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'p.product-title')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'ul > li.slide > a > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        texts = []
        element = of_utils.find_element_by_css_selector(driver, 'p.product-information')
        texts.append(element.text.strip())
        elements = of_utils.find_elements_by_css_selector(driver, 'table.gridtable > tbody > tr')
        for element in elements:
            _elements = of_utils.find_elements_by_css_selector(element, 'td')
            texts.append(_elements[0].text.strip() + _elements[1].text.strip())
        product['detail'] = '\n'.join(texts)
        return product