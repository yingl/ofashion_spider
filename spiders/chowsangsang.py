import sys
sys.path.append('../')
import of_spider
import of_utils

class ChowSangSang(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div#pdt-list-wrapper > div > div.item-blk > div > div.comp-pdt-blk-wrapper > a')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(4)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        driver.implicitly_wait(10)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h4.productSubheading.productDetails_Name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'h6.productSerial.productDetails_Style')
        if element:
            product['code'] = element.text.split('#')[-1].strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.productPrice > span.price')
        if element:
            try:
                price_text = element.text.strip()[1:].strip().replace(',', '')
                product['price_cny'] = int(float(price_text))
            except:
                pass
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div#product-preview-slider > div.slick-list > div > div.product-preview-slide.slick-slide > a')
        images = [element.get_attribute('href').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        texts = []
        elements = of_utils.find_elements_by_css_selector(driver, 'div.row-btm-3.text-subheading-1 > p')
        for element in elements:
            texts.append(element.get_attribute('innerHTML').strip())
        product['detail'] = '\n'.join(texts)
        return product