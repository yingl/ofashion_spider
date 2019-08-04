import sys
sys.path.append('../')
import of_spider
import of_utils

class Ipsa(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, '.list_pdt > li > a')
        arr = [element.get_attribute('href').strip() for element in elements]
        return {}.fromkeys(arr).keys()

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.detail_name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver,'.detail_options .ipsa_final_price')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.content_gallery_clone > .swiper-slide > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, '.detail_dscp')
        if element:
            product['detail'] = element.text.strip()
        return product
        
        