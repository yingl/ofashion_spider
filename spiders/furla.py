import sys
sys.path.append('../')
import of_spider
import of_utils

class Furla(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.product-image > a.thumb-link')
            if len(elements) > product_count:
                product_count = len(elements)
                # driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                driver.execute_script('arguments[0].scrollIntoView(true)', elements[-1])
                of_utils.sleep(4)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.product-name')
        if element:
            product['title'] = element.text.strip()
            element = of_utils.find_element_by_css_selector(driver, 'div#product-content > div.product-number')
            if element:
                product['title'] += ' ' + element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div#product-content >div.product-price > span.price-sales')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product-image > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        return product