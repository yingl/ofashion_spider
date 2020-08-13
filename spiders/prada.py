import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

class Prada(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        loadMore = of_utils.find_element_by_xpath(driver,'//div[@class="loadMore isVisible"]/button')
        if loadMore:
                driver.execute_script('arguments[0].click();', loadMore)
                of_utils.sleep(4)

        product_count = 0
        while True:
            elements = of_utils.find_elements_by_xpath(driver, '//a[@class="productQB__wrapperImage js-product-qb-link"]')
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
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver, '//h1[@class="pDetails__title"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver, '//div[@id="mainPdpContent"]')
        if element:
            product['code'] = element.get_attribute('data-partnumber')
        # price_cny
        element = of_utils.find_element_by_xpath(driver, '//div[@class=" pDetails__priceItem"]//span[@class="price__value"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver, '//div[@class="pDetails__slide js-imgProduct slick-slide"]//img')
        images = [element.get_attribute('src') for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail
        element = of_utils.find_element_by_xpath(driver, '//p[@class="pDetails__desc"]')
        if element:    
            product['detail'] = element.text.strip()
        return product