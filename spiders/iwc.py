import sys
sys.path.append('../')
import of_spider
import of_utils

class Iwc(of_spider.Spider):
    def parse_entry(self, driver):
        products = []
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.pack_shots > li> p.ref')
        for element in elements:
            ref = element.text.strip().split(' ')[-1]
            products.append(driver.driver.current_url + 'IW' + ref)
        return products

    def parse_product(self, driver):
        driver.implicitly_wait(10)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h2.pageTitle.watch-title')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'li.variation-reference > span.val')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'li.price > span.val')
        if element:
            try:
                price_text = element.text.strip()[1:].strip()
                product['price_cny'] = int(float(price_text))
            except:
                pass
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.frontBack > li > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.detailList > li')
        texts = [element.text.strip() for element in elements]
        product['detail'] = '\n'.join(texts).strip()
        return product