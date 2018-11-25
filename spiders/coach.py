import sys
sys.path.append('../')
import of_spider
import of_utils

class Coach(of_spider.Spider):
    def parse_entry(self, driver):
        products = []
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.product-list > li > div.img-box > a#product_detail_a')
        for element in elements:
            txt = element.get_attribute('name').strip()
            txt = txt.replace('\n', '')
            txt = txt.replace('\t', '')
            products.append('https://china.coach.com' + txt)
        return products

    def parse_product(self, driver):
        of_utils.sleep(5)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1#curr_skuName')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'p.pronumber')
        if element:
            product['code'] = element.text.split(':')[-1].strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'span.skuPrice')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'span.price#skuPrice')
        if element:
            price_text = element.text.strip()[3:].strip().replace(',', '') # 去掉开头的RMB
            product['price_cny'] = int(float(price_text))
        # images
        images = []
        elements = of_utils.find_elements_by_css_selector(driver, 'ul#fullscreen_swatchpro_small > li > img')
        for element in elements:
            txt = element.get_attribute('src').split('?')[0].strip()
            images.append(txt)
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.description')
        product['detail'] = element.text.strip()
        return product