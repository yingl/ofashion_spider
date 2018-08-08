import sys
sys.path.append('../')
import of_spider
import of_utils

class Loreal(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'a.link.product-title')
            if len(elements) > product_count:
                product_count = len(elements)
                btns = of_utils.find_elements_by_css_selector(driver, 'a.more-content')
                for btn in btns:
                    if btn.get_attribute('style'):
                        continue
                    driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(4)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'strong#productName')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_hkd
        element = of_utils.find_element_by_css_selector(driver, 'div.product-info__price')
        if element:
            price_text = element.text.split(' ')[0][1:].strip()
            product['price_hkd'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'article.product-large > div > div.media > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'p#productVariantName')
        product['detail'] = element.text.strip()
        return product