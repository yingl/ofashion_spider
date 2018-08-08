import sys
sys.path.append('../')
import of_spider
import of_utils

class Perregaux(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'div.item-list > ul > div > div > li.views-row  > div > div > div.field > div > div > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title/code
        elements = of_utils.find_elements_by_css_selector(driver, 'div.watch-intro-title > h1 > span')
        product['title'] = elements[1].text.strip()
        product['code'] = elements[2].text.strip().split(')')[1].strip()
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.watch-zoom > div > div.field-items > div > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.watch-presentation-content > div > div.field-items > div')
        product['detail'] = element.get_attribute('innerHTML').strip()
        return product