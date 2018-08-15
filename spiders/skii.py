import sys
sys.path.append('../')
import of_spider
import of_utils

class Skii(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'div.grid > div.product > a.product-link')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(10)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.pd__info__main > h1')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'div.product-name > h2')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.sizes > a.current')
        if element:
            try:
                price_text = element.get_attribute('data-price').replace(',', '')
                product['price_cny'] = int(float(price_text))
            except:
                pass
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.pd__info__photo > div.img > img')
        if not elements:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.left > div.img > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        texts = []
        elements = of_utils.find_elements_by_css_selector(driver, 'div.pd__info__main > p')
        if elements:
            for element in elements:
                text = element.text.strip()
                if text:
                    texts.append(text)
            product['detail'] = '\n'.join(texts)
        else:
            element = of_utils.find_element_by_css_selector(driver, 'div.box.description-box > p')
            product['detail'] = element.text.strip()
        return product