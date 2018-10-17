import sys
sys.path.append('../')
import of_spider
import of_utils

class Pinko(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'ul#search-result-items > li > div.product-tile > div.product-image > a')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('arguments[0].scrollIntoView(true)', elements[-1])
                of_utils.sleep(8)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.product-name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'span[itemprop=productID]')
        if element:
            product['code'] = element.text.strip()
        # price_cny N/A
        # images
        images = []
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product-image > picture > img')
        # images = [element.get_attribute('src').strip() for element in elements]
        for element in elements:
            image_text = element.get_attribute('src').strip()
            images.append(image_text.split('?')[0])
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.desc-image-wrap > div.product-description > p.product-description--content')
        product['detail'] = element.text.strip()
        return product