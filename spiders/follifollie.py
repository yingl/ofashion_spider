import sys
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
sys.path.append('../')
import of_spider
import of_utils


class FolliFollie(of_spider.Spider):
    def parse_entry(self, driver):
        btn = of_utils.find_element_by_css_selector(driver,'.view-all li a')
        if btn:
            driver.execute_script('arguments[0].click();', btn)
            of_utils.sleep(4)
        elements = of_utils.find_elements_by_css_selector(driver, "#search-result-items li a.thumb-link")
        return [element.get_attribute('href').strip() for element in elements]  

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        #title
        element = of_utils.find_element_by_css_selector(driver,'#product-content .product-name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        element = of_utils.find_element_by_css_selector(driver,'#product-content .product-number span')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '#product-content .product-price .price-sales')
        if element:
             product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '#pdpMain .primary-image')
        images = [element.get_attribute('src') for element in elements]
        images = {}.fromkeys(images).keys()
        product['images'] = ';'.join(images)
        # detail N/A
        return product
        
        