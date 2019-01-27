import sys
sys.path.append('../')
import of_spider
import of_utils

class BobbiBrown(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.product-grid__content > div.product-grid__item > div.product-thumb > a')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(4)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.product__title > h3.product_quickshop__header.product_quickshop__sub-line')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.js-product__info.product__info.desktop-block > div.product__price > span.price')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product-gallery__thumbs-row.slick-slide.slick-active > div > img')
        images = [element.get_attribute('src').strip() for element in elements]
        images = [image.replace('80x80', '415x415') for image in images]
        product['images'] = ';'.join(images)
        # detail N/A
        return product