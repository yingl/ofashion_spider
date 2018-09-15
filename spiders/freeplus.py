import sys
sys.path.append('../')
import of_spider
import of_utils

class FreePlus(of_spider.Spider):
    def parse_entry(self, driver):
        of_utils.sleep(5) # 必须等
        elements = of_utils.find_elements_by_css_selector(driver, 'ul > li.isotope-item > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.productName')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.productPriceArea > span')
        if element:
            price_text = element.text.strip().split('\u3000')[-1][:-1]
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.productPic > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'p.description')
        product['detail'] = element.text.strip()
        return product