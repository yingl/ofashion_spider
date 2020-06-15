import sys
sys.path.append('../')
import of_spider
import of_utils

class Ysl(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.products > article.item > a')
            if not elements:
                elements = of_utils.find_elements_by_css_selector(driver, 'div.plp-slide > div.thumbnail > div > a')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(20)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        if 'www.ysl.com' in driver.current_url:
            ele = of_utils.find_element_by_xpath(driver,'//meta[@property="og:title"]')
            if ele:
                product['title'] = ele.get_attribute('content')
            else:
                raise Exception('Title not found')
            
            ele = of_utils.find_element_by_xpath(driver,'//span[@class="modelFabricColor"]//span[@class="value"]')
            if ele:
                product['code'] = ele.get_attribute('innerHTML').strip()

            ele = of_utils.find_element_by_xpath(driver,'//div[@id="itemPrice"]') 
            if ele:
                txt = ele.get_attribute('innerHTML').strip()
                product['price_cny'] = of_utils.convert_price(txt[(txt.find('¥')+1):])

            eles = of_utils.find_elements_by_xpath(driver,'//ul[@class="alternativeImages"]//li//img[@class="mainImage"]')
            images = [e.get_attribute('data-origin').strip() if e.get_attribute('data-origin') else e.get_attribute('src')  for e in eles]
            product['images'] = ';'.join({}.fromkeys(images).keys())

        elif 'www.yslbeautycn.com' in driver.current_url:
            ele = of_utils.find_element_by_xpath(driver,'//div[@class="product-top"]//div[@class="product-tit"]//h1')
            if ele:
                product['title'] = ele.text.strip()
            else:
                raise Exception('Title not found')
            
            ele = of_utils.find_element_by_xpath(driver,'input[@id="hide-currentItemCode"]')
            if ele:
                product['code'] = ele.get_attribute('value')

            ele = of_utils.find_element_by_xpath(driver,'//div[@class="detail-item is-active current-item"]//p[@class="product-price"]')
            if ele:
                product['price_cny'] = of_utils.convert_price(ele.text.strip())

            eles = of_utils.find_elements_by_xpath(driver,'//div[@class="swiper-container e-main-scroll swiper-container-horizontal swiper-container-fade"]//div[@class="swiper-wrapper"]//img')
            images = [e.get_attribute('src').strip() for e in eles]
            product['images'] = ';'.join({}.fromkeys(images).keys())

            ele = of_utils.find_element_by_xpath(driver,'//div[@class="product-description none-sm"]/p')
            if ele:
                product['detail'] = ele.text.strip()

        return product