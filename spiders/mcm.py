import sys
sys.path.append('../')
import of_spider
import of_utils

class Mcm(of_spider.Spider):
    def parse_entry(self, driver):
        while True:
            element = of_utils.find_element_by_css_selector(driver, 'a.load-more')
            if element:
                driver.execute_script('arguments[0].click();', element)
                of_utils.sleep(3)
            else:
                break
        elements = of_utils.find_elements_by_css_selector(driver, 'div.grid-cell > a.thumb-link')
        if not elements:
            elements = of_utils.find_elements_by_css_selector(driver,'.mod_product_tile')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.product-name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'p.sku-id')
        if element:
            code_text = element.text.strip()
            code = code_text.split(' ')[-1].strip()
            product['code'] = code
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.product-price > span.price-sales')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        eles = of_utils.find_elements_by_css_selector(driver,'.js-main-image-container .main-pdp-image-slider .product-image img')
        images = [element.get_attribute('src').strip() for element in eles]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, '#panel1 p')
        if element:
            product['detail'] = element.text.strip()
        return product