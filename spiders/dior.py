import sys
sys.path.append('../')
import of_spider
import of_utils

class Dior(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product > div.product-image > a')
        if not elements:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.product > a.product-link')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver, '//div[@class="product-titles"]/h1/span')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver,'//p[@class="product-titles-ref"]')
        if element:
            product['code'] = element.text.strip().replace('编号: ','')
        # price_cny
        element = of_utils.find_element_by_xpath(driver, '//span[@class="price-line"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver, '//div[@class="image product-media__image"]/img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail
        element = of_utils.find_element_by_xpath(driver, '//div[@class="couture-description__html"]')
        if element:
            product['detail'] = element.get_attribute('innerHTML')
        return product