import sys
sys.path.append('../')
import of_spider
import of_utils

class Armani(of_spider.Spider):
    def parse_entry(self, driver):
        products = []
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, '.search-filter-and-search-results ul article a')
            if elements:
                for ele in elements:
                    if ele.get_attribute('href') != None:
                        products.append(ele.get_attribute('href').strip())
               
            btn = of_utils.find_element_by_css_selector(driver, '.nextPage>a')
            if not btn:
                of_utils.sleep(1)
                btn = of_utils.find_element_by_css_selector(driver, '.nextPage>a')
            if not btn:
                of_utils.sleep(1)
                btn = of_utils.find_element_by_css_selector(driver, '.nextPage>a')
            if not btn:
                of_utils.sleep(1)
                btn = of_utils.find_element_by_css_selector(driver, '.nextPage>a')
            if btn:
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(5)
            else:
                break
        return products

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.item-name>div>span')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'h1.item-name>span')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, '.item-model-code>div>span.value')
        if element:
            product['code'] = element.text.strip()
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.productImages ul li img')
        images = [element.get_attribute('data-origin').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, '.item-editorial-description>div>span')
        if element:
            product['detail'] = element.text.strip()
        return product