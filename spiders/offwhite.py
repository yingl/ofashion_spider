import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class Offwhite(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, '.products article.product a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '#RightRail #pdp_product_title')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, '.description-preview__style-color')
        if element:
            product['code'] = element.text.replace('款式：','').strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, "meta[property='og:price:amount']")
        if element:
            product['price_cny'] = element.get_attribute('content').strip()
        # images
        images = []
        elements = of_utils.find_elements_by_css_selector(driver, 'button.grid-image picture img')
        if elements:
            for ele in elements:
                img = ele.get_attribute('src')
                if img and 'PDP_LOADING' not in img:
                    images.append(img)
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, '.description-preview')
        if element:
            product['detail'] = element.text.strip()
        return product