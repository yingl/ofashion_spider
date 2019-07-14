import sys
sys.path.append('../')
import of_spider
import of_utils

class Rolex(of_spider.Spider):
    def parse_entry(self, driver):
        of_utils.sleep(10)
        elements = of_utils.find_elements_by_css_selector(driver,'.rlxr-watchgrid__watch-list-item>a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h2.rlxr-modelpage-majesty__watchname')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'p.productreference > span.productreference-value')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'span.rlxr-modelpage-majesty__price-num')
        if element:
            price_text = element.text.strip().replace('RMB', '').strip() # 去掉开头的¥
            product['price_cny'] = of_utils.convert_price(price_text)
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.rlxr-modelpage-majesty__figure>a>picture>img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, '.rlxr-modelpage-majesty__figure>a>figcaption')
        product['detail'] = element.text.strip()
        return product  