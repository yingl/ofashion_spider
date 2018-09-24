import sys
sys.path.append('../')
import of_spider
import of_utils

class Kiehls(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'div.b-product_tile > div > a.b-product_img-link')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h2.product_name > span.product_name')
        if element:
            product['title'] = element.get_attribute('innerHTML').strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.product-variations > div.price > p.product_price')
        if element:
            price_text = element.get_attribute('innerHTML').split('</span>')[-1]
            price_text = price_text[2:].strip()
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.l-product_details-left > div.product_image_container > div.product_primary_image > div > div > ul.overlay_carousel_items > li.overlay_carousel_item > a > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.b-product_description > div#tab_details > div.product_detail_description  > ul')
        product['detail'] = element.text.strip()
        return product