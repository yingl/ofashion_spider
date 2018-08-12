import sys
sys.path.append('../')
import of_spider
import of_utils

class StellaMccartney(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.products > li.products-item > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'span.modelName.inner')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.left > div.modelFabricColor > span.value')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.priceUpdater > span.price > span.value')
        if element:
            price_text = element.text.strip().replace(',', '')
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div#smc-yItemImages-thumbs > ul.alternativeImages > li > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.contentDesc > div.details > span.value')
        product['detail'] = element.get_attribute('innerHTML').strip().replace('<br>', '')
        return product