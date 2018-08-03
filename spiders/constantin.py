import sys
sys.path.append('../')
import of_spider
import of_utils

class Constantin(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.products > li > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.line1 > h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.reference > span')
        if element:
            product['code'] = element.text.strip().split(' ')[-1]
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div#priceDisplayValue')
        if element:
            try:
                price_text = element.text.strip()[1:].replace(",", '')
                product['price_cny'] = int(float(price_text))
            except:
                pass
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.callage > img.pngfix')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.listInfos.specifications > li')
        texts = [element.text.strip() for element in elements]
        product['detail'] = '\n'.join(texts).strip()
        return product