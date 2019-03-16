import sys
sys.path.append('../')
import of_spider
import of_utils

class Givenchy(of_spider.Spider):
    def parse_entry(self, driver):
        more_btn = of_utils.find_element_by_css_selector(driver, 'div.pagination > div.pager > a')
        if more_btn:
            driver.execute_script('arguments[0].click();', more_btn)
        of_utils.sleep(2)
        elements = of_utils.find_elements_by_css_selector(driver, 'figure.product-image  > a.thumb-link')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div#product-content > h1.product-name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.product-price > span.price-sales')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.swiper-slide > a.fullscreen > picture > img')
        images = [element.get_attribute('srcset').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        return product