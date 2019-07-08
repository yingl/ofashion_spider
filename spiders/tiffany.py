import sys
sys.path.append('../')
import of_spider
import of_utils

class Tiffany(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'article.product-tile>a')
            if len(elements) > product_count:
                product_count = len(elements)
                btn = of_utils.find_element_by_css_selector(driver, 'div.show-more>a')
                if btn:
                    driver.execute_script('arguments[0].click();', btn)
                else:
                    break
                of_utils.sleep(6)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.t1')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'h1.product-description__content_title')  
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div#itemPrice > div')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, '.pdp-price-details > span')
        if element:
            price_text = element.text.replace('¥','').strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.more-images > div.thumbs > div > img')
        images = []
        for element in elements:
            image = element.get_attribute('data-src')
            if image:
                images.append(image.strip())
        images = list(set(images))
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div#drawerDescription > div > div')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'p.product-description__container_long-desc')
        product['detail'] = element.text.strip()
        return product