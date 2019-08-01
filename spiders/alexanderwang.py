import sys
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
sys.path.append('../')
import of_spider
import of_utils

class AlexanderWang(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'ul.product-grid a.swiper-slide-active')
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
        return [ele.get_attribute('href').strip() for ele in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'article.product-details h1.product-details_name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product-details_price>span')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product-details-main-information_media>picture>img')
        if not elements:
            elements = of_utils.find_elements_by_css_selector(driver,'.product-details_images>picture>img')
        images = [element.get_attribute('src') if element.get_attribute('src') else 'https://www.alexanderwang.cn'+element.get_attribute('data-src')  for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, '.product-details-description>div>div')
        if element:
            product['detail'] = element.text.strip()
        return product