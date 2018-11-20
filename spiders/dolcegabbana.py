import sys
sys.path.append('../')
import of_spider
import of_utils

class DolceGabbana(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.b-product_tile > div > a.js-producttile_link')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(10)
            else:
                break
        return [element.get_attribute('href').strip().replace('/en/', '/zh/') for element in elements]

    def parse_product(self, driver):
        # Switch language
        btn = of_utils.find_element_by_css_selector(driver, 'span.b-country_language_selector-title')
        driver.execute_script('arguments[0].click();', btn)
        of_utils.sleep(3)
        link = of_utils.find_element_by_css_selector(driver, 'li.b-language_selector-language_item[data-locale=zh_TW] > a')
        driver.execute_script('arguments[0].click();', link)
        of_utils.sleep(5)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'span.b-product_name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.b-product_master_id')
        if element:
            product['code'] = element.text.split('：')[-1].strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'h2.b-product_container-price > div.b-product_price > h4.b-product_price-standard')
        if element:
            price_text = element.text.strip()[1:].strip().replace('.', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.js-thumbnails > li > img')
        images = []
        for element in elements:
            image = element.text.split('?')[0].strip()
            images.append(image)
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.b-product_long_description')
        text = element.get_attribute('innerHTML').strip()
        text = text.replace('<i>', '')
        text = text.replace('</i>', '')
        text = text.replace('<br>', '\n')
        texts = text.split('\n')
        detail_texts = []
        for text in texts:
            text = text.strip()
            if text != '':
                detail_texts.append(text)
        product['detail'] = '\n'.join(detail_texts)
        return product