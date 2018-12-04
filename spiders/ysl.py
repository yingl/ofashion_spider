import sys
sys.path.append('../')
import of_spider
import of_utils

class Ysl(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.products > article.item > a')
            if not elements:
                elements = of_utils.find_elements_by_css_selector(driver, 'div.plp-slide > div.thumbnail > div > a')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(20)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        of_utils.sleep(12) # Sleep for loading
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.productInfo > h1.productName > div > span.modelName')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'div.product-tit > h1')
        if element:
            product['title'] = element.text.strip()
            if not product['title']:
                product['title'] = element.get_attribute('innerHTML')
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.productInfo > div#itemPrice')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'div.product-handle > div.product-price')
        if element:
            price_text = element.text.strip()
            if price_text:
                price_text = price_text[1:].strip().replace(',', '') # 去掉开头的¥
                product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.itempage-images-content > ul.alternativeImages > li > img')
        if not elements:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.thumbnails-box > div > ul.swiper-wrapper > li > img')
            images = []
            for element in elements:
                img = element.get_attribute('src').strip()
                img = img.replace('110X110', '500X500')
                images.append(img)
        else:
            images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.description > div.descriptionContent')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'div.product-description > p')
            text = element.text.split('\n')[0].strip()
        else:
            text = element.text.strip()
        product['detail'] = text
        return product