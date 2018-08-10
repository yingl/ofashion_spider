import sys
sys.path.append('../')
import of_spider
import of_utils

class VanCleef(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'ul.product-list > li > div > div.product-image > a')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(6)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.popup-product-title > h2[itemprop=name]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.product-price > span.price > span')
        if element:
            price_text = element.text.strip()[1:].strip()
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.thumbs > ul > div > li > a > img')
        images = [element.get_attribute('src').strip().replace('w=118', 'w=1210') for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'p[itemprop=description]')
        product['detail'] = element.text.strip()
        return product