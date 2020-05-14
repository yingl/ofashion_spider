import sys
sys.path.append('../')
import of_spider
import of_utils

class AlexanderMcqueen(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(10)
        while True:
            loadMore = of_utils.find_element_by_xpath(driver,'//button[@class="component-load-more"]')
            if loadMore and loadMore.get_attribute('style') != 'display: none;':
                driver.execute_script('arguments[0].click();', loadMore)
                of_utils.sleep(5)
            else:
                break    

        elements = of_utils.find_elements_by_xpath(driver,'//a[@class="component-product-card"]')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver, '//h3[@class="component-products-head-line__title font-bemboStd"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver, '//p[@class="page-products-id__code"]')
        if element:
            product['code'] = element.text.strip().replace('商品代码：','')
        # price_cny
        element = of_utils.find_element_by_xpath(driver, '//div[@class="component-products-head-line__price"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver, '//li[@class="component-products-pictures__item"]/img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_xpath(driver, '//p[@class="page-products-id__describe"]')
        if element:
            product['detail'] = element.text.strip()
        return product
