import sys
sys.path.append('../')
import of_spider
import of_utils

class Dior(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product > div.product-image > a')
        if not elements:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.product > a.product-link')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.title-with-level > span')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'h1.title-with-level > span > span')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code Deal with detail
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.variation-option-price')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'div.product-actions>span')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'span.variation-option-price')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = of_utils.convert_price(price_text)
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product-image-grid > div[role=button] > div > div > img')
        if not elements:
            elements = of_utils.find_elements_by_css_selector(driver, 'ul > li.product-image-grid-image > button > div > div > img')
        if not elements:
            elements = of_utils.find_elements_by_css_selector(driver, 'button.product-media img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.product-tab-content > div.product-tab-html')
        texts =element.text.strip().split('\n')
        detail_texts = []
        for text in texts:
            if text:
                if text.startswith('编号'):
                    code = text.split(':')[-1].strip()
                    product['code'] = code
                else:
                    detail_texts.append(text)
        product['detail'] = '\n'.join(detail_texts)
        return product