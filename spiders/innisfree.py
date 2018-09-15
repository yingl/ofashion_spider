import sys
sys.path.append('../')
import of_spider
import of_utils

class InnisFree(of_spider.Spider):
    def parse_entry(self, driver):
        products = []
        elements = of_utils.find_elements_by_css_selector(driver, 'div.paging > a')
        if elements:
            pages = len(elements) - 2
            for i in range(pages):
                elements = of_utils.find_elements_by_css_selector(driver, 'div.paging > a')
                element = elements[1 + i]
                driver.execute_script('arguments[0].click();', element)
                of_utils.sleep(3)
                _elements = of_utils.find_elements_by_css_selector(driver, 'div.productList > ul > li > div.thumb > a')
                products.extend([element.get_attribute('href').strip() for element in _elements])
        else:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.list > ul > li > a')
            products = [element.get_attribute('href').strip() for element in elements]
        return products

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.productTitle > h3 > strong')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'dl.code > dd > span')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'dl.normalprice > dd')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.pdtVisual > h4 > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.pdtDesc > p.desc')
        product['detail'] = element.text.strip()
        return product