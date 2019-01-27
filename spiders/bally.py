import sys
sys.path.append('../')
import of_spider
import of_utils

class Bally(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'ul#product-search-result-items > li > article.product-tile > div > a.js-producttile_link')
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
        element = of_utils.find_element_by_css_selector(driver, 'h2.product-short-description')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'span[itemprop=price]')
        if element:
            price_text = element.get_attribute('content').strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.thumb.slick-active > img.productthumbnail')
        images = [element.get_attribute('src').strip() for element in elements]
        images = [image.split('?')[0] for image in images]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.js-preview-content > p')
        product['detail'] = element.text.strip()
        return product