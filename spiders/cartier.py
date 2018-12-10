import sys
sys.path.append('../')
import of_spider
import of_utils

class Cartier(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'div.grid-item > a.prod-link')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'span.c-pdp__cta-section--product-title')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.c-pdp__cta-section--product-ref-id > span')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.price')
        if element:
            price_text = element.get_attribute('innerHTML').strip()
            if not price_text.startswith('-￥'): # 有价格为-￥1的情况
                price_text = price_text[1:].strip().replace(',', '') # 去掉开头的¥
                product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.item.c-pdp__image--wrapper > div > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div#marketing_description > span')
        product['detail'] = element.text.strip()
        return product