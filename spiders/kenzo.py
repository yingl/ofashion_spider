import sys
sys.path.append('../')
import of_spider
import of_utils

class Kenzo(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.product-list > li > div.p-img > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.p-name > h3.subtitle')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.p-name > div.price')
        if element:
            price_text = element.text.strip().split(' ')[1].split('/')[0].strip()
            product['price_cny'] = int(price_text)
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.swiper-wrapper > li.swiper-slide > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.product-point > div#p-intro > div.des > p')
        product['detail'] = element.text.strip()
        return product