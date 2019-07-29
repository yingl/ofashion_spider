import sys
sys.path.append('../')
import of_spider
import of_utils

class DeBeers(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.component-grid-items > div > div.item > a')
            if not elements:
                elements = of_utils.find_elements_by_css_selector(driver,'.category-products>ul>li>a')
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
        element = of_utils.find_element_by_css_selector(driver, 'div.product-name > span.h1')
        if not element:
            element = of_utils.find_element_by_css_selector(driver,'.product-name>h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'span.sku')
        if element:
            product['code'] = element.text.split(':')[-1].strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'span.price')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.bxslider--new > div > a')
        if elements:
             images = [element.get_attribute('data-image').strip() for element in elements]
             product['images'] = ';'.join(images)
        else:
            elements = of_utils.find_elements_by_css_selector(driver,'div.product-image img')
            if elements:
                images = [element.get_attribute('src').strip() for element in elements]
                product['images'] = ';'.join(images)

        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div#product-description > div.textwrap > p')
        if element:
            product['detail'] = element.text.strip()
        return product