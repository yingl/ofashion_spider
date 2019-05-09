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
            elements = of_utils.find_elements_by_css_selector(driver, 'ul.products > li.item > div.imageContainer > a')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(4)
            else:
                break
        if not elements:
            while True:
                elements = of_utils.find_elements_by_css_selector(driver, 'div.product-image > div.swiper-wrapper > a.product-tile-link.swiper-slide-active')
                if len(elements) > product_count:
                    product_count = len(elements)
                    action = ActionChains(driver).move_to_element(elements[-1])
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
        element = of_utils.find_element_by_css_selector(driver, 'h1.productName > div.modelName > span')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.model > p.attributesUpdater.title > span.value')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.priceUpdater > span.full.price > span.value')
        if element:
            price_text = element.text.strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div#itemImages > ul.alternativeImages > li > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.ItemDescription > span.text')
        product['detail'] = element.text.strip()
        return product