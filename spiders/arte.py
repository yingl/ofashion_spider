import sys
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
sys.path.append('../')
import of_spider
import of_utils


class Arte(of_spider.Spider):
    def parse_entry(self, driver):
        urls = []
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, "ul.products>li>a") 
            for element in elements:
                urls.append(element.get_attribute('href').strip())
            btn = of_utils.find_element_by_css_selector(driver,'.next.page-numbers') 
            if btn:
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(4)
            else:
                break                   
        return urls

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        #title
        element = of_utils.find_element_by_css_selector(driver,'.product_title')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.entry-summary .price .woocommerce-Price-amount')
        if element:
             product['price_usd'] = element.text.replace('USD','').replace('$','').replace(',','').strip()
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.woo-variation-gallery-thumbnail-wrapper .slick-list .slick-slide img')
        images = [element.get_attribute('src').replace('-100x100','') for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        # of_utils.sleep(100)
        return product
        
        