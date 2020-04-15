import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Shuuemura(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        btn = of_utils.find_element_by_xpath(driver,'//a[@class="vew_all_articles hide-for-medium-only hide-for-small-l-only hide-for-small-m-only hide-for-small-only"]')
        if btn:
             driver.execute_script('arguments[0].click();', btn)
             of_utils.sleep(5)

        elements = of_utils.find_elements_by_xpath(driver,'//div[@class="c-product-tile__thumbnail b-product_img-topwrapper"]/a') 
        return [element.get_attribute('href').strip() for element in elements]  

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//h1[@class="c-product__subtitle product_subtitle"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver,'//h2[@class="c-product-tile__name-wrapper c-product__title product_name"]')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//div[contains(@class,"c-product__action-price")]//p')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//div[@class="show-for-medium-only"]//div[contains(@class,"js-carousel__item ")]/a')
        images = [element.get_attribute('href').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail
        element = of_utils.find_element_by_xpath(driver,'//div[@itemprop="description"]/p')
        if element:
            product['detail'] = element.text.strip()
        return product