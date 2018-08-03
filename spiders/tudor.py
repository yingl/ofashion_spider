import sys
sys.path.append('../')
import of_spider
import of_utils

class Tudor(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'div.tdr-watch > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'p.tdr-watch-details__header-watch-name > span')
        if element:
            product['title'] = element.text.strip().replace('\n', '')
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'p.tdr-watch-details__header-watch-reference')
        if element:
            product['code'] = element.text.strip().split('：')[-1]
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.tdr-variations__main-image-canvas-wrapper > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        texts = []
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.tdr-watch-details__column > li > div.tdr-watch-details__text')
        for element in elements:
            k_element = of_utils.find_element_by_css_selector(element, 'p.tdr-watch-details__title')
            v_element = of_utils.find_element_by_css_selector(element, 'p.tdr-watch-details__spectext')
            texts.append(k_element.text.strip() + '：' + v_element.text.strip())
        product['detail'] = '\n'.join(texts)
        return product