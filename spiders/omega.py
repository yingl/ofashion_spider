import sys
sys.path.append('../')
import of_spider
import of_utils

class Omega(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'ol.products > li.item.product > div > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'span.product.attribute.name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'span.value[itemprop=sku]')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'span.product-price-reveal__action__show')
        if element:
            driver.execute_script('arguments[0].click();', element)
            of_utils.sleep(2)
            element = of_utils.find_element_by_css_selector(driver, 'span.price')
            if element:
                price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
                product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.fotorama__stage__shaft > div > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product-info-details-content > div.value > p')
        texts = [element.get_attribute('innerHTML').strip() for element in elements]
        product['detail'] = '\n'.join(texts)
        return product