import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class Valentino(of_spider.Spider):
    def parse_entry(self, driver):
        urls = []
        driver.implicitly_wait(10)

        while True:
            loadMore = of_utils.find_element_by_css_selector(driver,'.loadMore button')
            if loadMore:
                driver.execute_script('arguments[0].click();', loadMore)
                of_utils.sleep(2)
            else:
                break    

        elements = of_utils.find_elements_by_css_selector(driver, '.producList .product .productInfo .style')
        for i in range(0,len(elements)):
            d = of_utils.create_chrome_driver()
            d.implicitly_wait(10)
            d.get(driver.current_url)

            while True:
                loadMore = of_utils.find_element_by_css_selector(d,'.loadMore button')
                if loadMore:
                    d.execute_script('arguments[0].click();', loadMore)
                    of_utils.sleep(2)
                else:
                    break   

            eles = of_utils.find_elements_by_css_selector(d, '.producList .product .productInfo .style')
            d.execute_script('arguments[0].click();', eles[i]) 
            urls.append(d.current_url)
            print(d.current_url)
            d.close()
        return urls

    def parse_product(self, driver):
        driver.implicitly_wait(15)
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