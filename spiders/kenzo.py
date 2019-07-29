import sys
sys.path.append('../')
import of_spider
import of_utils

class Kenzo(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.product-list > li > div.p-img > a')
        if not elements:
            product_count = 0
            while True:
                elements = of_utils.find_elements_by_css_selector(driver, '.category-products-container a.product')
                if len(elements) > product_count:
                    product_count = len(elements)
                    driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                    of_utils.sleep(4)
                else:
                    break   

        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.p-name > h3.subtitle')
        if not element:
            element = of_utils.find_element_by_css_selector(driver,'.productpage-fiche-inner h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver,'.productpage-fiche-ref p')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.p-name > div.price')
        if element:
            price_text = element.text.strip().split(' ')[1].split('/')[0].strip()
            product['price_cny'] = of_utils.convert_price(price_text)

        # price_euro_de
        element = of_utils.find_element_by_css_selector(driver, '.productpage-fiche-price .price')
        if element:
            product['price_euro_de'] = element.text.strip().replace('€','')

        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.swiper-wrapper > li.swiper-slide > img')
        if not elements:
            elements = of_utils.find_elements_by_css_selector(driver,'.productpage-images .productpage-image img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.product-point > div#p-intro > div.des > p')
        if element:
            product['detail'] = element.text.strip()
        else:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.product-point > div#p-intro > div.des > div')
            texts = [element.text.strip() for element in elements]
            product['detail'] = '\n'.join(texts)
        return product