import sys
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
sys.path.append('../')
import of_spider
import of_utils


class Cpb(of_spider.Spider):
    def parse_entry(self, driver):
        btn = of_utils.find_element_by_css_selector(driver, '.c-product-cards-list-all')
        if btn:
            driver.execute_script('arguments[0].click();', btn)
            of_utils.sleep(4)

        elements = of_utils.find_elements_by_css_selector(driver,'.c-product-cards-list-item .c-product-cards-photo-img')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, ".product-name")
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.price-sales')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.c-block-shopingmodal-main-thumbnail .slick-list .slick-slide img')
        if elements:
            images = [element.get_attribute('src').strip() for element in elements]
            product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver,'.c-block-richcontent-text')
        if element:
            product['detail'] = element.text.strip()
        return product
        
        