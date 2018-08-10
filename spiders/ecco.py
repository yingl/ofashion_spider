import sys
sys.path.append('../')
import of_spider
import of_utils

class Ecco(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'ul.search-result-items > li > div.product-tile > div > div.product-image > a.thumb-link')
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
        element = of_utils.find_element_by_css_selector(driver, 'h1.product-name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.styleNumber > value')
        if element:
            product['code'] = element.text.strip()[1:].strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'span.product-price-normal')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '')
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'li.thumb > a.thumbnail-link')
        images = [element.get_attribute('href').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        texts = []
        element = of_utils.find_element_by_css_selector(driver, 'div.desktop-DescriptionSection > div.detail-block > p')
        texts.append(element.text.strip())
        elements = of_utils.find_elements_by_css_selector(driver, 'div.desktop-DescriptionSection > div.detail-block > div.more-details > ul > li')
        for element in elements:
            texts.append(element.text.strip())
        product['detail'] = '\n'.join(texts)
        return product