import sys
sys.path.append('../')
import of_spider
import of_utils

class Puma(of_spider.Spider):
    def parse_entry(self, driver):
        products = []
        element = of_utils.find_element_by_css_selector(driver, 'div.page-last.page-icon')
        pages = int(element.get_attribute('totalpage'))
        for i in range(pages):
            elements = of_utils.find_elements_by_css_selector(driver, 'div.search-result-content > ul > li > div > div > div > a.thumb-link')
            for element in elements:
                products.append(element.get_attribute('href').strip())
            next_btn = of_utils.find_element_by_css_selector(driver, 'div.page-next')
            driver.execute_script('arguments[0].click();', next_btn)
        return products

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.goods_about > p.about_tit')
        if element:
            product['title'] = element.text.strip().replace('\n', ' ')
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'p.bianhao > span')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'p.about_cost > span')
        if element:
            price_text = element.text.strip()[1:].strip()
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.swiper-wrapper > li > img')
        images = [element.get_attribute('src').strip().replace('80X80', '540X540') for element in elements]
        product['images'] = ';'.join(images)
        # detail
        elements = of_utils.find_elements_by_css_selector(driver, 'div.word > div > p > span')
        texts = [element.text.strip() for element in elements]
        product['detail'] = '\n'.join(texts)
        return product