import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class victoriasSecret(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_xpath(driver, '//div[@class="productList-img"]/a')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(5)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        of_utils.sleep(5)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//i[@class="iconfont icon-ICON_share"]/..')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver,'//div[@class="code"]')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//div[@class="product-price"]/i')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//ul[@class="small-img-list"]/li/img')
        images = [element.get_attribute('data-src').strip().split('?x-oss-process')[0] for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        element = of_utils.find_element_by_xpath(driver,'//div[@class="desc"]//div[@class="content"]')
        if element:
            product['detail'] = element.text.strip()
        return product