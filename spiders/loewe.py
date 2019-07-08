import sys
sys.path.append('../')
import of_spider
import of_utils

class Loewe(of_spider.Spider):
    def parse_entry(self, driver):
        view_all = of_utils.find_element_by_css_selector(driver, 'span.js-view-all-products')
        driver.execute_script('arguments[0].click();', view_all)
        of_utils.sleep(3)
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.product-tile > figure.product-image > a.thumb-link')
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
        element = of_utils.find_element_by_css_selector(driver, 'div#product-content > div > h1.product-name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        elements = of_utils.find_elements_by_css_selector(driver, 'div.details-table > ul.details-col-2 > li')
        if len(elements) >= 2:
            element = elements[1]
            product['code'] = element.text.split(':')[-1].strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.price-and-size-wrapper > div.product-price > span.price-sales')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.lw-pdp-container-images > div.js-show-zoom > picture > img')
        if not elements:
            element = of_utils.find_element_by_css_selector(driver, 'div.product-image-container > picture > img')
            elements = [element]
            _elements = of_utils.find_elements_by_css_selector(driver, 'div.js-show-zoom > picture > img')
            elements += _elements
        images = [element.get_attribute('src').strip() for element in elements]
        images = list(set(images))
        product['images'] = ';'.join(images)
        # detail N/A
        return product
