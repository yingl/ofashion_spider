import sys
sys.path.append('../')
import of_spider
import of_utils

class Coach(of_spider.Spider):
    def parse_entry(self, driver):
        products = []
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.product-list > li > div.img-box > a#product_detail_a')
        for element in elements:
            txt = element.get_attribute('name').strip()
            txt = txt.replace('\n', '')
            txt = txt.replace('\t', '')
            products.append('https://china.coach.com' + txt)
        return products

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.cel-Product-infosName')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, '#curr_skuName')
        if element:
            product['title'] = element.get_attribute('innerHTML').strip()
        else:
            raise Exception('Title not found')
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.product-price>p')
        if element:
            price_text = element.get_attribute('data-gtm-product-sales-price').strip()
            product['price_cny'] = of_utils.convert_price(price_text)
        else:    
            element = of_utils.find_element_by_css_selector(driver, '#skuPrices')
            price_text = element.get_attribute('value').strip().replace(',','')
            product['price_cny'] = of_utils.convert_price(price_text)
        # code
        element = of_utils.find_element_by_css_selector(driver, '#styleCode')
        if element:
        product['code'] = element.get_attribute('value').strip()
        # images
        main_img = of_utils.find_element_by_css_selector(driver, '#main_image').get_attribute('src').strip()
        elements = of_utils.find_elements_by_css_selector(driver, 'div.smallimg ul>li>a>img')
        images = [element.get_attribute('lazy_src').strip() for element in elements] if elements else []
        product['images'] = main_img + ';' + ';'.join(images)
        return product