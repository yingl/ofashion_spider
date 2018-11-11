import sys
sys.path.append('../')
import of_spider
import of_utils

class VanCleef(of_spider.Spider):
    def parse_entry(self, driver):
        # 手袋
        elements = of_utils.find_elements_by_css_selector(driver, 'div.fs-products-grid__product.fs-gridelement > div.fs-products-grid__product__illu > a')
        if not elements:
            # 彩妆
            elements = of_utils.find_elements_by_css_selector(driver, 'div.fnb_col-wd6.fnb_product-img > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'span.fs-productsheet__title') # 手袋
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'span.fnb_pdp-subtitle') # 彩妆
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.fs-productsheet__ref')
        if element:
            product['code'] = element.text.split(':')[-1].strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'p.fnb_pdp-price')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        images = []
        elements = of_utils.find_elements_by_css_selector(driver, 'li.fs-productsheet__zoom__content-li > div.fs-productsheet__zoom__sizeArea > div > div > picture')
        if elements:
            for element in elements:
                _element = of_utils.find_element_by_css_selector(element, 'source')
                images.append(_element.get_attribute('data-srcset').strip())
        else:
            element = of_utils.find_element_by_css_selector(driver, 'a.fnb_thumbnail-img > img')
            images.append(element.get_attribute('src').strip())
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.fnb_description-left  > div > div.row > div > p')
        if element:
            product['detail'] = element.text.strip()
        return product