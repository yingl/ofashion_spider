import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Zenith(of_spider.Spider):
    def parse_entry(self, driver):
        of_utils.sleep(5)
        elements = of_utils.find_elements_by_xpath(driver, '//div[@class="swiper-wrapper"]/div/div/a') 
        return [element.get_attribute('href').strip() for element in elements]  

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//section[@class="section-product_resume main-section"]/h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver,'//section[@class="section-product_resume main-section"]/span')
        if element:
            product['code'] = element.text.strip()
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_xpath(driver, '//div[@class="product_hero"]/img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail
        element = of_utils.find_element_by_xpath(driver,'//section[@class="section-product_resume main-section"]/p')
        if element:
            product['detail'] = element.text.strip()
        return product
