import sys
sys.path.append('../')
import of_spider
import of_utils

class Gucci(of_spider.Spider):
    def parse_entry(self, driver):
        btn = of_utils.find_element_by_css_selector(driver, 'div.spice-looks-grid-button > a')
        if btn:
            driver.execute_script('arguments[0].click();', btn) # 点击“浏览所有”
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.spice-float-clearfix > li > div > div > a.spice-item-grid')
        if not elements:
            elements = of_utils.find_elements_by_css_selector(driver, 'div#pdlist > div.grid-cell > div.product-tiles-box > a.spice-item-grid')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.spice-product-name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.spice-style-number-title > span')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.spice-product-price > span')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'img.spice-smart-zoom')
        images = list(set([element.get_attribute('srcset').strip() for element in elements]))
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.spice-description-small > p')
        product['detail'] = element.get_attribute('innerHTML').strip()
        return product