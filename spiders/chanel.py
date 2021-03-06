import sys
sys.path.append('../')
import of_spider
import of_utils

class Chanel(of_spider.Spider):
    def parse_entry(self, driver):
        # 手袋
        elements = of_utils.find_elements_by_css_selector(driver, 'div.fs-products-grid__product.fs-gridelement > div.fs-products-grid__product__illu > a')
        if not elements:
            # 手袋2
            elements = of_utils.find_elements_by_css_selector(driver, 'div.fs-products-grid > div.fs-products-grid__product.fs-gridelement > div.fs-products-grid__product__wrapper > a')
        if not elements:
            # 彩妆
            elements = of_utils.find_elements_by_css_selector(driver, 'div.fnb_col-wd6.fnb_product-img > a') 
        # 手表
        if not elements:
            load_more = of_utils.find_element_by_css_selector(driver, 'div.pd-action-btns > button[role=button]')
            if not load_more: # 戒指
                load_more = of_utils.find_element_by_css_selector(driver, 'div.display-all > a')
            if load_more:
                driver.execute_script('arguments[0].click();', load_more)
            of_utils.sleep(5)
            product_count = 0
            while True:
                elements = of_utils.find_elements_by_css_selector(driver, 'div.products > div.row > div > ul > li > div.product-item-wrapper > a')
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
        element = of_utils.find_element_by_css_selector(driver, 'span.fs-productsheet__title') # 手袋
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'span.fnb_pdp-subtitle') # 彩妆
        if not element:
            element = of_utils.find_element_by_css_selector(driver, '#product-details dl dd:nth-of-type(1)') # 手表
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.fs-productsheet__ref')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, '#product-details dl dd:nth-of-type(2)') # 手表
        if element:
            product['code'] = element.text.split(':')[-1].strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'p.fnb_pdp-price')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'span.fs-productsheet__price_value.fs-price__value')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'div.product-price') # 手表
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '').replace('*', '') # 去掉开头的¥
            product['price_cny'] = of_utils.convert_price(price_text)
        # images
        images = []
        elements = of_utils.find_elements_by_css_selector(driver, '.fs-productsheet__slideshow--desktop > ul > li picture ')
        
        if elements:
            for element in elements:
                _element = of_utils.find_element_by_css_selector(element, 'source')
                images.append(_element.get_attribute('srcset').strip())
        else:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.product-images figure>a>img') # 手表
            if elements:
                for element in elements:
                    images.append(element.get_attribute('src').strip())        
            else:
                element = of_utils.find_element_by_css_selector(driver, 'a.fnb_thumbnail-img > img')
                images.append(element.get_attribute('src').strip())
        product['images'] = ';'.join(images)

        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.fnb_description-left  > div > div.row > div > p')
        if element:
            product['detail'] = element.text.strip()
        return product