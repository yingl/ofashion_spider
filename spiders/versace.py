import sys
sys.path.append('../')
import of_spider
import of_utils

class Versace(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'article.product-tile a.js-producttile_link')
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
        element = of_utils.find_element_by_css_selector(driver, 'div#product-content h1.product-name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div#product-content p.js-product-number')
        if element:
            product['code'] = element.text.strip().replace('产品：','')
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div#product-content div.product-price>span')
        if element:
            price_text = element.get_attribute('content')
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.product-images-section .pdp-gallery-item>a>img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div#product-content div.product-description')
        product['detail'] = element.text.strip()
        return product