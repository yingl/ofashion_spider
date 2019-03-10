import sys
sys.path.append('../')
import of_spider
import of_utils

class Burberry(of_spider.Spider):
    def parse_entry(self, driver):
        btns = of_utils.find_elements_by_css_selector(driver, 'a.shelf_view-all')
        for btn in btns:
            driver.execute_script('arguments[0].click();', btn)
            of_utils.sleep(4)
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product_container > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
        of_utils.sleep(6)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.product-purchase_name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'p.product-purchase_item-number')
        if element:
            product['code'] = element.text.split(' ')[-1].strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'span.product-purchase_price')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        cover_images = of_utils.find_elements_by_css_selector(driver, 'div.product-carousel_item > picture > img')
        other_images = of_utils.find_elements_by_css_selector(driver, 'ul.product-gallery > li > div > picture > img')
        elements = cover_images + other_images
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.accordion-tab_content > p')
        product['detail'] = element.text.strip()
        return product