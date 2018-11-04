import sys
sys.path.append('../')
import of_spider
import of_utils

class Dsquared2(of_spider.Spider):
    def parse_entry(self, driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'ul.products > li > div.search-item-container > a.search-item-link')
            if len(elements) == product_count:
                break
            else:
                product_count = len(elements)
            more_button = of_utils.find_element_by_css_selector(driver, 'button.search-loadmore-label')
            if more_button:
                driver.execute_script('arguments[0].click();', more_button)
                of_utils.sleep(5)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        of_utils.sleep(5)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.breadcrumbLeaf > p.attributesUpdater.Title > span.value')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.item-alternativeImages-shots > ul > li > img')
        print(elements)
        images = []
        for element in elements:
            image = element.get_attribute('data-origin').strip().replace('_10_', '_20_')
            images.append(image)
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'span.modelName')
        product['code'] = element.get_attribute('innerHTML').strip() # Code here...
        btn = of_utils.find_element_by_css_selector(driver, 'ul.itemDetails-info-accordion > li > h2 > div.plusIcon')
        driver.execute_script('arguments[0].click();', btn)
        elements = of_utils.find_elements_by_css_selector(driver, 'div.itemdescription > ul > li')
        texts = [element.get_attribute('innerHTML').strip() for element in elements]
        product['detail'] = '\n'.join(texts)
        return product