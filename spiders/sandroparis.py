import sys
sys.path.append('../')
import of_spider
import of_utils

class SandroParis(of_spider.Spider):
    def parse_entry(self, driver):
        products = []
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product-image > div.table-cell > a')
        for element in elements:
            products.append(element.get_attribute('href').strip())

        while True:     
            page = of_utils.find_element_by_css_selector(driver, 'div.pagination > ul.clearfix > li > a.page-next')
            if page:
                page.click()
                of_utils.sleep(4)
                elements = of_utils.find_elements_by_css_selector(driver, 'div.product-image > div.table-cell > a')
                for element in elements:
                    products.append(element.get_attribute('href').strip())
            else:
                break
        return products
        
    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1#title')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_xpath(driver, '//span[@class="price-sales"]')
        if element:
            product['price_cny'] =  of_utils.convert_price( element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.productSlide > li > a > div.zoomPad > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'h2.detaildesc')
        product['detail'] = element.text.strip()
        return product