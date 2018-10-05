import sys
sys.path.append('../')
import of_spider
import of_utils

class HugoBoss(of_spider.Spider):
    def parse_entry(self, driver):
        for i in range(3):
            driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
            of_utils.sleep(4)
        elements = of_utils.find_elements_by_css_selector(driver, 'div#search-result-items > div.grid-tile >  div.product-tile > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.productName')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.product-number')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div#product-content > div.product-price')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            price_text = price_text.split('\n')[0].strip()
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.swiper-wrapper > div.swiper-slide > img.productthumbnail')
        images = [element.get_attribute('src').strip() for element in elements]
        images = list(set(images))
        product['images'] = ';'.join(images)
        # detail
        detail_block = of_utils.find_elements_by_css_selector(driver, 'div.accordion > div')[2]
        element = of_utils.find_element_by_css_selector(detail_block, 'div.accordion__item__text > p')
        text = element.get_attribute('innerHTML').strip()
        text = text.replace('<br>', '')
        product['detail'] = text
        return product