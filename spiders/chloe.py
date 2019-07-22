import sys
sys.path.append('../')
import of_spider
import of_utils

class Chloe(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'article.item > div > a')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(4)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        of_utils.sleep(5)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.productName > div > span.modelName')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.itemBoxPrice > div > div.itemPrice > span.price > span.value')
        if element:
            price_text = element.text.strip().replace(',', '')
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.productAlternative .slick-track .thumbWrap img')
        images = []
        for element in elements:
            img = element.get_attribute('src').strip().replace('_8_', '_22_')
            images.append(img)
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.itemdescription > span.value')
        text = element.get_attribute('innerHTML').strip()
        text = text.replace('<br><br>', '<br>')
        texts = text.split('<br>')
        for text in texts:
            if text.startswith('商品编号'):
                code = text.split('：')[-1].strip()
                product['code'] = code
        product['detail'] = '\n'.join(texts)
        return product