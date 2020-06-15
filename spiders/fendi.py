import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

class Fendi(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_xpath(driver, '//a[@class="product-item"]')
            if len(elements) > product_count:
                product_count = len(elements)
                action = ActionChains(driver).move_to_element(elements[-1])
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.perform()
                of_utils.sleep(4)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver, '//div[@class="product-info-section"]//h1[@class="product-name"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver, '//span[@class="product-sku"]')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_xpath(driver, '//div[@class="product-info-section"]//span[@class="price bold-family"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver, '//div[contains(@class,"swiper-item cursor-zoom swiper-slide")]/img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_xpath(driver, '//div[@class="item-description"]/div')
        if element:
            product['detail'] = element.text.strip()
        return product