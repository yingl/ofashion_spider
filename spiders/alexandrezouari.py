import sys
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
sys.path.append('../')
import of_spider
import of_utils


class AlexandreZouari(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, "td.font_content>table.font_productname>tbody>tr>td>a") 
        return [element.get_attribute('href').strip() for element in elements] 

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        #title
        product['title'] = driver.title.replace('Alexandre Zouari -','').strip()
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.font_productprice>b')
        if element:
             product['price_hkd'] = element.text.replace('HKD','').replace(',','').strip()
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'tr[valign="top"]>td>table:not(.font_producttext)>tbody>tr>td>a>img')
        images = [element.get_attribute('src') for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        return product
        
        