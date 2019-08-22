import sys
sys.path.append('../')
import of_spider
import of_utils

class Mtm(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, "#goods .product-list a") 
        return [element.get_attribute('href').strip() for element in elements]  

    def parse_product(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver,'.product_list .product_1 a')
        flag = int(driver.current_url.split('?')[-1])
        element = elements[flag]
        driver.execute_script('arguments[0].click();', element)
        of_utils.sleep(2)

        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.popup_product_%s .product_detail_content .jspPane h2' % flag)
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.popup_product_%s .product_photo h3' % flag)
        if element:
             product['price_hkd'] = element.text.strip().split('/')[0].strip().replace('$','').replace(',','')
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.popup_product_%s .product_photo img' % flag)
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        return product