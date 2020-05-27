import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

class Thomaspink(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        while True:
            loadMore = of_utils.find_element_by_xpath(driver,'//pink-listing-view-more/a/button')
            if loadMore:
                driver.execute_script('arguments[0].click();', loadMore)
                of_utils.sleep(5)
            else:
                break    

        elements = of_utils.find_elements_by_xpath(driver,'//a[@class="product-result_image-link js-gtm-click"]')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver,'//h1[@class="product-detail_name"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver,'//p[contains(@class,"itemNum")]')
        if element:
            product['code'] = element.text.strip().replace('ITEM: ','')
        # price_cny
        element = of_utils.find_element_by_xpath(driver,'//div[@class="product-detail_price"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip().replace('CN¥‌',''))
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//img[@class="product-imagery_picture-image"]')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail N/A
        element = of_utils.find_element_by_xpath(driver,'//div[contains(@class,"description")]/p')
        if element:
            product['detail'] = element.text.strip()
        return product