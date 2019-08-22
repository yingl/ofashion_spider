import sys
sys.path.append('../')
import of_spider
import of_utils

class Msgm(of_spider.Spider):
    def parse_entry(self, driver):
        while True:
            btn = of_utils.find_element_by_css_selector(driver,'.paging_tab_loadmore')
            if btn:
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(4)
            else:
                break    

        elements = of_utils.find_elements_by_css_selector(driver, "#container_gallery .vaschetta_item_img a")      
        return [element.get_attribute('href').strip() for element in elements]   

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.details_info_title>h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver,'.details_info_code')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.details_price_new>span')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip().replace(',00','').replace('.',''))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.MagicZoom > figure > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver,'.details_info_descr')
        if element:
            product['detail'] = element.text.strip()
        return product