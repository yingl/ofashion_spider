import sys
sys.path.append('../')
import of_spider
import of_utils

class Swarovski(of_spider.Spider):
    def parse_entry(self, driver):
        products = []
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div#listpage > div.listproduct > a')
            products.extend([element.get_attribute('href').strip() for element in elements])
            btn_next = of_utils.find_element_by_css_selector(driver, 'li.arrow > a.next')
            if not btn_next: # Actually break here
                break
            curr_page = btn_next.get_attribute('data-current-page')
            page_count = btn_next.get_attribute('data-page-count')
            if curr_page < page_count:
                driver.execute_script('arguments[0].click();', btn_next)
                of_utils.sleep(3)
            else:
                break
        return products

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1[itemprop=name]')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'ul.desc-features > li')
        if element:
            product['code'] = element.text.split(':')[-1].strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'p.price[itemprop=price]')
        price_text = element.text.strip().split(' ')[-1].replace(',', '')
        product['price_cny'] = int(float(price_text))
        # images
        images = []
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.thumbnails > li > a > img')
        for element in elements:
            image_text = element.get_attribute('src').strip()
            image_text = image_text.replace('/080/', '/BestView/')
            image_text = image_text.replace('-W080', '')
            images.append(image_text)
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'span[itemprop=description]')
        product['detail'] = element.text.strip()
        return product