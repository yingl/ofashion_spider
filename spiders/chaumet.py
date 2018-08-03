import sys
sys.path.append('../')
import of_spider
import of_utils

class Chaumet(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'ul#grid > li > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.product-card > span')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'span.reference-jewelry')
        if element:
            product['code'] = element.text.strip()
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.content > img.carousel-slide__media')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        texts = []
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.fiche-details__left > li')
        for element in elements:
            k_element = of_utils.find_element_by_css_selector(element, 'span')
            v_element = of_utils.find_element_by_css_selector(element, 'p')
            texts.append(k_element.text.strip() + '：' + v_element.text.strip())
        product['detail'] = '\n'.join(texts)
        return product