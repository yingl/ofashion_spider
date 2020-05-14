import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class Valentino(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(10)

        while True:
            loadMore = of_utils.find_element_by_xpath(driver,'//div[@class="loadMore"]/button')
            if loadMore:
                driver.execute_script('arguments[0].click();', loadMore)
                of_utils.sleep(5)
            else:
                break    

        elements = of_utils.find_elements_by_xpath(driver,'//div[@class="blankDiv"]/a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        of_utils.sleep(5)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, ".detail-title")
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.detail-price > span')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.prod-media-mainImg > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        return product