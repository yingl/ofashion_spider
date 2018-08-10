import sys
sys.path.append('../')
import of_spider
import of_utils

class Pomellato(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'ul.products  > li.item > div > a')
            if len(elements) > product_count:
                product_count = len(elements)
                view_more = of_utils.find_element_by_css_selector(driver, 'div.viewmore > span.label')
                if view_more:
                    driver.execute_script('arguments[0].click();', view_more)
                else:
                    driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(5)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.productName.itemTitle')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.editorial-description > div > span.value')
        if element:
            product['code'] = element.text.split(' ')[-1].strip()
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div#productSecondaryImage > ul.alternativeImages > li > img')
        images = [element.get_attribute('src').strip().replace('_8_', '_17_') for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.description > div.title > span.value')
        product['detail'] = element.text.strip()
        return product