import sys
sys.path.append('../')
import of_spider
import of_utils

class IsaKnox(of_spider.Spider):
    def parse_entry(self, driver):
        products = []
        pages = of_utils.find_elements_by_css_selector(driver, 'table.table-page > tbody > tr > td > a')
        if pages:
            for i in range(len(pages)):
                pages = of_utils.find_elements_by_css_selector(driver, 'table.table-page > tbody > tr > td > a')
                pages[i].click()
                elements = of_utils.find_elements_by_css_selector(driver, 'div.project-obj > div > a')
                products.extend([element.get_attribute('href').strip() for element in elements])
        else:
            products = [element.get_attribute('href').strip() for element in elements]
        return products

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.right[align=left] > div')
        if element:
            texts = element.text.split('\n')
            product['title'] = ' '.join(texts[:-1])
            price_text = texts[-1].split('/')[0].split('$')[-1].strip()
            product['price_hkd'] = int(float(price_text))
        else:
            raise Exception('Title not found')
        # code N/A
        # price_hkd Processed in title
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.left[align=center] > div >img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        texts = []
        elements = of_utils.find_elements_by_css_selector(driver, 'table.table-productdetails > tbody > tr > td')
        for element in elements:
            text = element.text.strip()
            if text:
                texts.append(text)
        product['detail'] = '\n'.join(texts)
        return product