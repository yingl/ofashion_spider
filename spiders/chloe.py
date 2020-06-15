import sys
sys.path.append('../')
import of_spider
import of_utils
import of_errors

class Chloe(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'article.item > div > a')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(4)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver, '//h1[@class="productName "]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_xpath(driver, '//div[@class="itemBoxPrice"]//span[@class="price"]//span[@class="value"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver,'//ul[@class="alternativeImages"]//li//img')
        images = [element.get_attribute('src').strip() if element.get_attribute('src') else element.get_attribute('data-origin')  for element in elements]
        product['images'] = ';'.join({}.fromkeys(images).keys())
        # detail
        element = of_utils.find_element_by_xpath(driver, '//div[@class="attributesUpdater itemdescription"]//span[@class="value"]')
        if element:
            txt = element.get_attribute('innerHTML').strip()
            product['detail'] = txt
            product['code'] = txt[txt.find('商品编号')+5:] if txt.find('商品编号') >= 0 else ''
        return product