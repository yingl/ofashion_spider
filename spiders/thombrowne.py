import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
import json

class ThomBrowne(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        elements = of_utils.find_elements_by_css_selector(driver, "div[data-test='ProductListingPage-productsWrapper']>div>article>a")
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, "h1[data-test='ProductDetailPage-productName']")
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, "span[data-test='ProductDetailPage-productPrice']")
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.swiper-wrapper picture source')
        images = [element.get_attribute('srcset').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        return product