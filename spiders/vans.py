import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class Vans(of_spider.Spider):
    def parse_entry(self, driver):
        while True:
            btn = of_utils.find_element_by_css_selector(driver,'#load_more')
            if btn and '查看更多' in btn.text.strip():
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(4)
            else:
                break    

        elements = of_utils.find_elements_by_css_selector(driver, "#gallery_show .goods-item .goods-pic a:not(.fast-Shop)")      
        return [element.get_attribute('href').strip() for element in elements]     

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.product-titles>h2')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.action-price')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.replace('C','').replace('$','').strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.thumbnail-list>ul>li>div.thumbnail>a>img')
        images =  [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        return product