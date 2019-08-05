import sys
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
sys.path.append('../')
import of_spider
import of_utils


class Narshk(of_spider.Spider):
    def parse_entry(self, driver):
        urls = []
        elements = of_utils.find_elements_by_css_selector(driver, '.imgshow')
        for ele in elements:
             driver.execute_script('arguments[0].click();', ele)
             of_utils.sleep(1)
             urls.append(driver.current_url)
             closeBtn = of_utils.find_element_by_css_selector(driver,'.product-close')
             driver.execute_script('arguments[0].click();', closeBtn)
        return urls

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, ".product-title")
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product-price-discount .product-price-val')
        if element:
            product['price_hkd'] = element.text.strip()[3:]
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.product-cover')
        if elements:
            images = [element.get_attribute('src').strip() for element in elements]
            product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver,'.product-description')
        if element:
            product['detail'] = element.text.strip()
        return product
        
        