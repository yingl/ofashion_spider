import sys
sys.path.append('../')
import of_spider
import of_utils

class JeanRichard(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div#watch-selector-list > a')
            if len(elements) > product_count:
                product_count = len(elements)
                btn = of_utils.find_element_by_css_selector(driver, 'button#more-watches')
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(4)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(10)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.hidden-xs[itemprop=name]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'p.reference > span.ezstring-field')
        if element:
            product['code'] = element.text.strip()
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.watch > img[itemrprop=image]')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        texts = []
        elements = of_utils.find_elements_by_css_selector(driver, 'div.details > div >  div.ezxmltext-field > p')
        for element in elements:
            text = element.text.strip()
            if text:
                texts.append(text)
        product['detail'] = '\n'.join(texts)
        return product