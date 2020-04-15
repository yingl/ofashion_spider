import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Dickies(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        urls = []
        while True:
            elements = of_utils.find_elements_by_xpath(driver, '//div[@class="good-card__img"]/a')
            if elements:
                for ele in elements:
                    urls.append( ele.get_attribute('href').strip())

            btn = of_utils.find_element_by_xpath(driver,'//ul[@class="sp-pagination clearfix fr goods-page"]/li[5]')
            if btn and btn.get_attribute('class') !='disable':
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(5)
            else:    
                break
        return {}.fromkeys(urls).keys()

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//h2[@class="goods-title"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver,'//div[@class="goods-bn"]')
        if element:
            product['code'] = element.text.strip().replace('ITEM: ','')
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//span[@class="price-primary sp-price sp-price__default clearfix"]/span[@class="price__int"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//div[@class="img-container"]/img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        return product