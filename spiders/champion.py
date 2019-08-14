import sys
sys.path.append('../')
import of_spider
import of_utils

class Champion(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, '.link-image-holder')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '#prod__title')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.current_price')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.replace('Sale','').replace('price','').replace('CNY','').strip())
        # product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        images = []
        elements = of_utils.find_elements_by_css_selector(driver, '#s7dpv-swatches-1 .s7thumb')
        for ele in elements:
            txt = ele.get_attribute('style')
            if 'background-image' in txt:
                images.append(txt[txt.index('background-image')+23:-3].replace('wid=75','wid=600').replace('hei=75','hei=600'))
        product['images'] = ';'.join(images)
        # detail N/A
        return product