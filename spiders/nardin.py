import sys
sys.path.append('../')
import of_spider
import of_utils

class Nardin(of_spider.Spider):
    def parse_entry(self, driver):
        products = []
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.view-content > div > div > span > a.watch-content')
            for element in elements:
                products.append(element.get_attribute('href'))
            next_btn = of_utils.find_element_by_css_selector(driver, 'a[title="Go to next page"]')
            if next_btn:
                driver.execute_script('arguments[0].click();', next_btn)
                of_utils.sleep(4)
            else:
                break
        return products

    def parse_product(self, driver):
        driver.implicitly_wait(10)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'span.title-category')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'span.title-ref')
        if element:
            product['code'] = element.text.split(' - ')[0].strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.watch-price > div.watch-price-value')
        if element:
            price_text = element.text.strip().replace("'", '')
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.slick-track[role=listbox] > div > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        texts = []
        elements = of_utils.find_elements_by_css_selector(driver, 'div.specs-content > p')
        for element in elements:
            text = element.get_attribute('innerHTML').strip()
            if text:
                texts.append(text)
        product['detail'] = '\n'.join(texts)
        return product