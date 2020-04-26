import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Benefitcosmetics(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_xpath(driver, '//a[@class="product-small-link"]')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//div[contains(@class,"product-details-desktop")]//h1[@class="parent-product-name"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver,'//li[@class="carousel-image slick-slide slick-active slick-current"][1]')
        if element:
            product['code'] = element.get_attribute('data-sku')
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//div[contains(@class,"product-details-desktop")]//div[@class="price"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//div[@class="product-image-box"]/img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        element = of_utils.find_element_by_xpath(driver,'//meta[@name="description"]')
        if element:
            product['detail'] = element.get_attribute('content')
        return product