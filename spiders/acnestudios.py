import sys
sys.path.append('../')
import of_spider
import of_utils

class AcneStudios(of_spider.Spider):
    def parse_entry(self, driver):
        of_utils.sleep(8)
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.product-image > a.thumb-link')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(4)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        of_utils.sleep(12)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.product-item__detail-name > div.product-name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'p.productreference > span.productreference-value')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.product-item__detail-name > div.product-price > span.price-sales')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'div.product-item__detail-price > div.product-price > span.price-sales')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product-item__gallery-item-image > a > img')
        images = ['https://www.acnestudios.com' + element.get_attribute('data-zoom-src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.product-item__core-information > div > div.product-item__detail-info-description')
        product['detail'] = element.text.strip()
        return product