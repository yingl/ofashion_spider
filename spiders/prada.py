import sys
sys.path.append('../')
import of_spider
import of_utils

class Prada(of_spider.Spider):
    def parse_entry(self, driver):
        btn = of_utils.find_element_by_css_selector(driver, 'button#viewAll')
        if btn:
            driver.execute_script('arguments[0].click();', btn)
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.product-img > a')
            if len(elements) > product_count:
                product_count = len(elements)
                btn = of_utils.find_element_by_css_selector(driver, 'button#discoverMore')
                if btn:
                    driver.execute_script('arguments[0].click();', btn)
                else:
                    break
                of_utils.sleep(6)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.entry-title')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.container > div.pdp-name > p.pdp-sku')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.container > div.pdp-name > p.pdp-price')
        if element:
            price_text = element.get_attribute('innerHTML').strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.stiky-style-images > a.inventoryVariant > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        texts = []
        elements = of_utils.find_elements_by_css_selector(driver, 'div.pdp-tab-longdesc > ul > li')
        for element in elements:
            texts.append(element.text.strip())
        product['detail'] = '\n'.join(texts)
        return product