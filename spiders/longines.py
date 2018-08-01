import sys
sys.path.append('../')
import of_spider
import of_utils

class Longines(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'ol.product-items > li > div > div.details > a.product-item-link')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'li.item.category128 > a')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'li.item.product')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.product-info-price > div > div.price-box > span > span > span.price')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'img.fotorama__img')
        if elements:
            images = [element.get_attribute('src').strip() for element in elements]
        else:
            elements = of_utils.find_elements_by_css_selector(driver, 'ul.newpdp-gallery-slider > li > img')
            images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail 格式非常不友好，暂时不处理！
        return product