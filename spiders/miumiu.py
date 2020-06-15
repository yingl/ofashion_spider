import sys
sys.path.append('../')
import of_spider
import of_utils

class MiuMiu(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        while True:
            loadMore = of_utils.find_element_by_xpath(driver,'//div[@class="o-viewMore"]')
            if loadMore and 'display: none;' not in loadMore.get_attribute('style'):
                loadMore = of_utils.find_element_by_xpath(driver,'//div[@class="o-viewMore"]/a')
                driver.execute_script('arguments[0].click();', loadMore)
                of_utils.sleep(5)
            else:
                break    

        elements = of_utils.find_elements_by_xpath(driver,'//a[@class="js-product-link"]')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver, '//div[@class="c-product-details"]//h1[@class="c-title"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver, '//div[@class="c-cod"]')
        if element:
            product['code'] = element.text.replace('货号','').strip()
        # price_cny
        element = of_utils.find_element_by_xpath(driver, '//span[@class="c-realprice"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver, '//div[@class="c-vertical-scroll js-init-slick"]/div[@class="c-slide"]/span/img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_xpath(driver,'//h2[@class="c-description"]')
        if element:
            product['detail'] = element.text.strip()
            # product['detail'] = element.get_attribute('innerHTML').strip()
        return product