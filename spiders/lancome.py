import sys
sys.path.append('../')
import of_spider
import of_utils

class Lancome(of_spider.Spider):
    def parse_entry(self, driver):
        products = []
        elements = of_utils.find_elements_by_css_selector(driver, 'div.list-product > div > div.plp-slide > div > div > a.modUrl')
        for element in elements:
            products.append(element.get_attribute('href').strip() )
        return products

    def parse_product(self, driver):
        driver.implicitly_wait(10)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.product-tit > h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.left-box.priceAndNum > span.product-price')
        if element:
            try:
                price_text = element.text.strip()[1:].strip()
                product['price_cny'] = int(float(price_text))
            except:
                pass
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.master-map-container > div > ul.swiper-wrapper > li > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'ul.tabs-container > li > div.text-box')
        product['detail'] = element.text.strip()
        return product