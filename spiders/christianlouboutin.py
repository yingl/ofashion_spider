import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class ChristianLouboutin(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, '#category-main .product a')
            if len(elements) > product_count:
                product_count = len(elements)
                action = ActionChains(driver).move_to_element(elements[-1])
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.perform()
                of_utils.sleep(4)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.page-header .title-cap')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.primary-details .price-box .price')
        if element:
            product['price_usd'] = of_utils.convert_price(element.text.replace('C','').replace('$','').strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.product-main>.swiper-container>.swiper-wrapper>img')
        images =  [element.get_attribute('src').strip() for element in elements]
        images = {}.fromkeys(images).keys()
        product['images'] = ';'.join(images)
        # detail N/A
        element = of_utils.find_element_by_css_selector(driver,'.description')
        if element:
            product['detail'] = element.text.strip()
        return product