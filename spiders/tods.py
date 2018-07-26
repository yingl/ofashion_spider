import sys
sys.path.append('../')
import of_spider
import of_utils

class Tods(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.row.prodotti > div.containerListedProduct > div > a')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(4)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.subtitle')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'p.sku_subtitle')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'span#final-price')
        if element:
            price_text = element.text.strip()[1:].strip() # 去掉开头的¥
            product['price_cny'] = int(price_text)
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div#carouselProductImage > div.caroufredsel_wrapper > ul > li > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.descriptionBox > p.descriptionText')
        product['detail'] = element.text.strip()
        return product