import sys
sys.path.append('../')
import of_spider
import of_utils

class Hublot(of_spider.Spider):
    def parse_entry(self, driver):
        of_utils.sleep(8)
        elements = of_utils.find_elements_by_css_selector(driver, 'div.owl-next')
        for element in elements:
            for _ in range(20): # Just hard code...
                driver.execute_script('arguments[0].click();', element)
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product-list > a')
        return list(set([element.get_attribute('href').strip() for element in elements]))

    def parse_product(self, driver):
        of_utils.sleep(5)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.page-header__title > span')
        if element:
            product['title'] = element.text.strip()
            element = of_utils.find_element_by_css_selector(driver, 'div.product-heading-content > span')
            if element:
                product['title'] += ' ' + element.text.strip()
        else:
            raise Exception('Title not found')
        # code Process it later...
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.page-header__img-wrapper.js-img-wrapper > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        texts = []
        elements = of_utils.find_elements_by_css_selector(driver, 'div.block-technical__content-list > div > ul')
        for element in elements:
            _elements = of_utils.find_elements_by_css_selector(element, ' ul.vertical-list__sub-list > li')
            for _element in _elements:
                prop = of_utils.find_element_by_css_selector(_element, 'h4').text.strip()
                value = of_utils.find_element_by_css_selector(_element, 'p').text.strip()
                if prop == '编号':
                    product['code'] = value
                else:
                    texts.append(prop + '：' + value)
        product['detail'] = '\n'.join(texts)
        return product