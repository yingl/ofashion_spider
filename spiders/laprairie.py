import sys
sys.path.append('../')
import of_spider
import of_utils

class Laprairie(of_spider.Spider):
    def parse_entry(self, driver):
        eles = of_utils.find_elements_by_css_selector(driver,'.product-tile__image-link')
        return [ele.get_attribute('href').strip() for ele in eles]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver, '//h2[@class="product-hero__name title-big title-big--thin"]')
        if element:
            product['title'] = element.get_attribute('innerHTML').strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '#product-content .product-price .price-sales')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        element = of_utils.find_element_by_css_selector(driver,"meta[property='og:image']")
        if element:
            product['images'] = element.get_attribute('content').strip()
        # detail N/A
        return product