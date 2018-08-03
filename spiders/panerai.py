import sys
sys.path.append('../')
import of_spider
import of_utils

class Panerai(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.pan-prod-ref-collection-list > div > li > div > div > figure > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.pan-ref-detail-name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'h6.pan-ref-prod-id')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'span.pan-ref-product-price')
        price_text = element.text.strip()[1:].replace(",", '')
        product['price_cny'] = int(float(price_text))
        # images
        images = []
        elements = of_utils.find_elements_by_css_selector(driver, 'div[data-component-name=referencegallery] > div.pan-carousel > div > div.slick-list[aria-live=polite] > div.slick-track > div')
        for element in elements:
            desc = element.get_attribute('aria-describedby')
            if desc:
                desc = desc.strip()
                if desc.startswith('slick-slide'):
                    element_ = of_utils.find_element_by_css_selector(element, 'figure > picture > img')
                    images.append('https://www.panerai.cn' + element_.get_attribute('srcset').strip())
        product['images'] = ';'.join(images)
        # detail
        texts = []
        elements = of_utils.find_elements_by_css_selector(driver, 'div.pan-technical-spec-left > div.pan-technical-spec-list')
        elements.extend(of_utils.find_elements_by_css_selector(driver, 'div.pan-technical-spec-right > div.pan-technical-spec-list'))
        for element in elements:
            k_element = of_utils.find_element_by_css_selector(element, 'h6')
            if not k_element:
                continue
            v_element = of_utils.find_element_by_css_selector(element, 'p')
            texts.append(k_element.text.strip() + '：' + v_element.text.strip())
        product['detail'] = '\n'.join(texts)
        return product