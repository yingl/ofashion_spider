import sys
sys.path.append('../')
import of_spider
import of_utils

class Hermes(of_spider.Spider):
    def parse_entry(self, driver):
        driver.implicitly_wait(15)
        load_more = of_utils.find_element_by_css_selector(driver, 'button.load-more-button')
        if load_more:
            driver.execute_script('arguments[0].click();', load_more)
        of_utils.sleep(5)
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'ul.product-grid-list.grid-list > li > article.product-item > a')
            if not elements:
                elements = of_utils.find_elements_by_css_selector(driver, 'div.product-item > a')
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
        element = of_utils.find_element_by_xpath(driver, '//div[@id="variant-info"]/h1')
        if not element:
            element = of_utils.find_element_by_xpath(driver, '//p[@class="product-title"]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver, '//div[@id="product-detail"]//div[@class="commerce-product-sku"]/p/span')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_xpath(driver, '//div[@id="variant-info"]/p[@class="field-type-commerce-price"]')
        if not element:
            element = of_utils.find_element_by_xpath(driver, '//p[@class="product-price"]')
        if element:
             product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_xpath(driver, '//picture[@class="product-item-picture"]/img')
        if not elements:
            elements = of_utils.find_elements_by_xpath(driver, '//img[contains(@class,"main-product-image")]')
        if elements:
            images = [element.get_attribute('src').strip() for element in elements if 'data:image/gif' not in element.get_attribute('src')]
            product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_xpath(driver, '//div[@class="field-name-field-description"]/div/p')
        if not element:
            element = of_utils.find_element_by_xpath(driver, '//p[@class="product-attribute-font-description"]')
        if element:
            product['detail'] = element.text.strip()
        return product