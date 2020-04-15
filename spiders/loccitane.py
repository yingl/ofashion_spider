import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Loccitane(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        urls = []
        while True:
           
            elements = of_utils.find_elements_by_xpath(driver, '//div[@class="goods-pic"]/a')
            if elements:
                for ele in elements:
                    url = ele.get_attribute('href').strip()
                    if url == 'javascript:;':
                        url = 'https://www.loccitane.cn' + ele.get_attribute('onclick').strip().replace('listGoUrl(\'','').replace('\')','')
                    urls.append(url)

            btn = of_utils.find_element_by_xpath(driver,'//a[@class="flip next"]')
            if btn:
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(5)
            else:    
                break
        return urls

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//div[@class="product-titles"]/h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//ins[@class="action-price"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//div[@class="product-album-pic"]/a/img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        return product