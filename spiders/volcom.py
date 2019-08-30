import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class Volcom(of_spider.Spider):
    def parse_entry(self, driver):
        urls = []
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, '.ProductTile__image-container')
            if elements:
                for ele in elements:
                    urls.append(ele.get_attribute('href').strip())
            btn = of_utils.find_element_by_css_selector(driver,'span.next>a')
            if btn:
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(4)
            else:    
                break
        return urls

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '#ProductInfo .ProductHeading__title')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, "meta[property='og:price:amount']")
        if element:
            product['price_usd'] =int(float(element.get_attribute('content')))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.ProductImages__image--desktop')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        return product