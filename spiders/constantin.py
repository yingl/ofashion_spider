import sys
sys.path.append('../')
import of_spider
import of_utils

class Constantin(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        elements = of_utils.find_elements_by_xpath(driver, '//a[@class="rcms_seeproduct"]')            
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//div[@class="detail__title"]/h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver,'//div[@class="detail__reference"]/span')
        if element:
            product['code'] = element.text.strip().replace('编号','')
        # price_cny
        element = of_utils.find_element_by_xpath(driver, '//div[@class="detail__price"]/h3')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver, '//img[@class="img-margin-fix_pdp lazyautosizes lazyloaded"]')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        return product