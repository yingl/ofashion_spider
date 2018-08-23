import sys
sys.path.append('../')
import of_spider
import of_utils

class Guerlain(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'div.category-products > ul > li.item > div > div.p_content > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.product-titles > div.product-name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.price-info > div.price-box > span.regular-price')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        element = of_utils.find_element_by_css_selector(driver, 'li.product-img.main-pic > img')
        product['images'] = element.get_attribute('src').strip()
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.tab_content > div[data-anchor-scroll-id=desc] > div')
        product['detail'] = element.text.split('\n')[1].strip()
        return product