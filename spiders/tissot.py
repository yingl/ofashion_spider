import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class Tissot(of_spider.Spider):
    def parse_entry(self, driver):
        urls = []
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'ul.products-grid>li>div>a ')
            if elements:
                for ele in elements:
                    urls.append(ele.get_attribute('href').strip())
            btn = of_utils.find_element_by_css_selector(driver,'.toolbar-bottom .pager .pages .i-next')
            if btn:
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(4)
            else:    
                break
        return urls

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.product-shop>div.product-name>h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        element = of_utils.find_element_by_css_selector(driver, '.product-shop>div.product-sku')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product-shop>div.price-wrapper>.price-box>span>span.price')
        if element:
            product['price_cny'] =  of_utils.convert_price(element.text.strip())
        # # images
        elements = of_utils.find_elements_by_css_selector(driver, '.move-view-slide .item img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # # detail N/A
        return product