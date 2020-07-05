import sys
sys.path.append('../')
import of_spider
import of_utils

class Ysl(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        while True:
            loadMore = of_utils.find_element_by_xpath(driver,'//a[@class="btn-load-more"]')
            if loadMore and "display: none;" not in loadMore.get_attribute('style'):
                driver.execute_script('arguments[0].click();', loadMore)
                of_utils.sleep(5)
            else:
                break    

        elements = of_utils.find_elements_by_xpath(driver,'//a[@class="component-product-card"]')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        if 'www.ysl.cn' in driver.current_url:
            ele = of_utils.find_element_by_xpath(driver,'//h2[@class="page-products-id__title"]')
            if ele:
                product['title'] = ele.text.strip()
            else:
                raise Exception('Title not found')
            
            ele = of_utils.find_element_by_xpath(driver,'//ul[@class="page-products-id__text__material-color"]/li/span[2]')
            if ele:
                product['code'] = ele.get_attribute('innerHTML').strip()

            ele = of_utils.find_element_by_xpath(driver,'//div[@class="page-products-id__price"]/span') 
            if ele:
                product['price_cny'] = of_utils.convert_price(ele.text.strip())

            eles = of_utils.find_elements_by_xpath(driver,'//ul[@class="component-products-pictures__desktop layout-desktop-large-desktop-only"]//li//img')
            images = [e.get_attribute('src')  for e in eles if 'base64,' not in e.get_attribute('src')]
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