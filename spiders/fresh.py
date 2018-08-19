import sys
sys.path.append('../')
import of_spider
import of_utils

class Fresh(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.search-result-items > li > div.product-tile > div.product-image > a.thumb-link')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.product-name > span')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.product-price > span')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product-primary-image > a[name=product_detail_image] > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        texts = []
        element = of_utils.find_element_by_css_selector(driver, 'section.shadow-wrapper > p.product-description')
        if element:
            text = element.text.strip()
            if text:
                texts.append(text)
        elements = of_utils.find_elements_by_css_selector(driver, 'section.shadow-wrapper > p > span')
        for element in elements:
            text = element.text.strip()
            if text:
                texts.append(text)
        product['detail'] = '\n'.join(texts)
        return product