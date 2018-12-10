import sys
sys.path.append('../')
import of_spider
import of_utils

class Boucheron(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'div.products-list > div > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.product-main-bloc > div > div > h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        element = of_utils.find_element_by_css_selector(driver, 'p.reference > span')
        if element:
            product['code'] = element.text.strip()
        # price_cny N/A
        # images
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.product-media > img')
            images = [element.get_attribute('src').strip() for element in elements]
            print(images[0])
            if not images[0].endswith('.gif'):
                break
            else:
                of_utils.sleep(5)
        # detail
        texts = []
        element = of_utils.find_element_by_css_selector(driver, 'p.shortDescription')
        texts.append(element.get_attribute('innerHTML').strip())
        element = of_utils.find_element_by_css_selector(driver, 'div.box-collateral > p')
        texts.append(element.get_attribute('innerHTML').strip())
        product['detail'] = '\n'.join(texts)
        return product