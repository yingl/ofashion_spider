import sys
sys.path.append('../')
import of_spider
import of_utils

class DanielWellington(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'div.products > div.summary-product-list > div.product > a[style="opacity: 1; visibility: visible"]')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.product-title.desktop > div.inner > h1[lang=en]')
        if element:
            product['title'] = element.text.strip().replace('\n', ' ')
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'img.main-image')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        texts = []
        element = of_utils.find_element_by_css_selector(driver, 'div.readmore')
        texts.append(element.text.strip())
        elements = of_utils.find_elements_by_css_selector(driver, 'div.list-details > div.row')
        for element in elements:
            spans = of_utils.find_elements_by_css_selector(element, 'span')
            texts.append(spans[0].text.strip() + '：' + spans[1].text.strip())
        product['detail'] = '\n'.join(texts)
        return product