import sys
sys.path.append('../')
import of_spider
import of_utils

class Patek(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.products > li > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1[dir=ltr] > span.complication')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.article_ref > span.reference')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'span#product_price')
        if element:
            price_text = element.get_attribute('innerHTML').strip().split(' ')[0].replace("'", '')
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.intro_images > div > div.slick-track > div > div > picture > img')
        images = [element.get_attribute('data-src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        elements = of_utils.find_elements_by_css_selector(driver, 'div.article_content > p')
        texts = [element.text.strip() for element in elements]
        product['detail'] = '\n'.join(texts).strip()
        return product