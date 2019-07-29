import sys
sys.path.append('../')
import of_spider
import of_utils

class Iwc(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, '.iwc-finder-result-products .iwc-finder-result-product .iwc-finder-product-link')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(10)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.iwc-buying-options-title')
        if element:
            product['title']  = element.text.strip().replace('\n添加至我的愿望清单','')
        else:
            raise Exception('Title not found')        
        # code
        element = of_utils.find_element_by_css_selector(driver, '.iwc-buying-options-reference')
        if element:
            product['code'] = element.text.strip()
            product['title'] =  product['title'] + ' ' + element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.iwc-buying-options-price')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.iwc-buying-option-thumbnails .iwc-watch-thumbnail-container:not(.slick-cloned) .iwc-watch-thumbnail')
        images = ['https://www.iwc.cn'+ element.get_attribute('data-srcset').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.detailList > li')
        texts = [element.text.strip() for element in elements]
        product['detail'] = '\n'.join(texts).strip()
        return product