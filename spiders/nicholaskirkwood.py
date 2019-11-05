import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class Nicholaskirkwood(of_spider.Spider):
    def parse_entry(self, driver):
        of_utils.sleep(8)
        elements = of_utils.find_elements_by_css_selector(driver, "article>div>a") 
        return [element.get_attribute('href').strip() for element in elements]  

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'meta[property="og:title"]')
        if element:
            product['title'] = element.get_attribute('content')
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'meta[property="product:price:amount"]')
        if element:
            product['price_cny'] = int(float(element.get_attribute('content')))
        # # images
        elements = of_utils.find_elements_by_css_selector(driver, 'main>div>div>div>div>img')
        if elements:
            images = [element.get_attribute('src').strip() for element in elements]
            product['images'] = ';'.join(images)
        # # detail N/A
        return product