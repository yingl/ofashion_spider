import sys
sys.path.append('../')
import of_spider
import of_utils

class Cartier(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'div.grid-item > a.prod-link')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//h1[@class="c-pdp__cta-section--product-title js-pdp__cta-section--product-title"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver,'//span[@class="local-ref"]')
        if element:
            product['code'] = element.text.strip().replace('编号: ','')
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//div[@class="price js-product-price-formatted"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver, '//div[@class="c-pdp__product-carousel js-pdp__product-carousel carousel slide"]//img[@class="image js-adaptiveImage c-pdp__image image"]')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_xpath(driver, '//div[@class="tabbed-content__content-column"][1]/p')
        if element:
            product['detail'] = element.text.strip()
        return product