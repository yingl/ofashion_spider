import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class Y3(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, '.products>li>article>figure>div>a')
        return [element.get_attribute('href').strip() for element in elements]

    #TODO 获取价格获取不到，被监测到了 
    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        elements = of_utils.find_elements_by_css_selector(driver, '.item-name-line')
        txts = [element.text.strip() for element in elements]
        if txts:
            product['title'] = ' '.join(txts)
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.item-price .itemPrice .price .value')
        if element:
            product['price_hkd'] = element.text.strip()
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.item-zoom-images>ul.alternativeImages>li>img')
        images =  [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, '.editorialdescription>span.value')
        if element:
            product['detail'] = element.text.strip()
        return product