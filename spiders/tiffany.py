import sys
sys.path.append('../')
import of_spider
import of_utils

class Tiffany(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'a.itemDiv')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.t1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div#itemPrice > div')
        if element:
            price_text = element.text.split(' ')[-1].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.more-images > div.thumbs > div > img')
        images = []
        for element in elements:
            image = element.get_attribute('data-src')
            if image:
                images.append(image.strip())
        images = list(set(images))
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div#drawerDescription > div > div')
        product['detail'] = element.text.strip()
        return product