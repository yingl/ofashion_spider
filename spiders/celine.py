import sys
sys.path.append('../')
import of_spider
import of_utils

class Celine(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'article.product-tile > a')
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
        element = of_utils.find_element_by_css_selector(driver, 'h1.cel-Product-infosName')
        if element:
            product['title'] = element.get_attribute('innerHTML').strip()
        else:
            raise Exception('Title not found')
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.product-price>p')
        price_text = element.get_attribute('data-gtm-product-sales-price').strip()
        if price_text:
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product-primary-image ul > li >button > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        return product