import sys
sys.path.append('../')
import of_spider
import of_utils

class HamiltonWatch(of_spider.Spider):
    def parse_entry(self, driver):
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.loadmore')
            if elements:
                for element in elements:
                    driver.execute_script('arguments[0].click();', element)
                    of_utils.sleep(2)
            else:
                break
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.products-grid > li.item > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.product-title > h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'span.regular-price > span.price')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '')
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div#product-page-top > div > div > div > div > div > div > img')
        if not elements:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.img-cont > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div#product-description')
        product['detail'] = element.text.strip()
        return product