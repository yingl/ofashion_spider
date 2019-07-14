import sys
sys.path.append('../')
import of_spider
import of_utils

class Montblanc(of_spider.Spider):
    def parse_entry(self, driver):
        while True:
            btn = of_utils.find_element_by_css_selector(driver, '.mb-load-more')
            if btn:
                if not btn.get_attribute('style'):
                    driver.execute_script('arguments[0].click();', btn)
                    of_utils.sleep(4)
                else:
                    break    
            else:
                break          
        elements = of_utils.find_elements_by_css_selector(driver, '.mb-prod-tile-section > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.mb-pdp-heading')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code 
        element = of_utils.find_element_by_css_selector(driver, '.mb-pdp-prod-ident')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.mb-pdp-price')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.slick-slide:not(.slick-cloned) img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        return product