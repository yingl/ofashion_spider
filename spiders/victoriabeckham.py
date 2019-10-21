import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class VictoriaBeckham(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, ".grid__item .product-card > a") 
        return [element.get_attribute('href').strip() for element in elements]  

    def parse_product(self, driver):
        btn = of_utils.find_element_by_css_selector(driver,'.glCancelBtn')
        if btn:
            driver.execute_script('arguments[0].click();', btn)
            of_utils.sleep(2)

        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.product-title')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_gbp
        element = of_utils.find_element_by_css_selector(driver, '.dark-happy-place--grey-med>span')
        if element:
            product['price_gbp'] =  element.text.replace('£','').replace(',','').replace('.00','').strip()
        # # images
        elements = of_utils.find_elements_by_css_selector(driver, '.product__image-wrapper ul li img')
        images = [element.get_attribute('data-src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # # detail N/A
        return product