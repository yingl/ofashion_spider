import sys
sys.path.append('../')
import of_spider
import of_utils

class Dhc(of_spider.Spider):
    def parse_entry(self, driver):
        products = []
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.pro-list-right > ul > li > a')
            for element in elements:
                products.append(element.get_attribute('href').strip())
            btns = of_utils.find_elements_by_css_selector(driver, 'div.page-box > a')
            if btns:
                btn = btns[-1]
                if btn.text.strip() == '<下一页>':
                    driver.execute_script('arguments[0].click();', btn)
                    of_utils.sleep(4)
                else:
                    break
            else:
                break
        return products

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.detail-label > span')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code + price_cny
        elements = of_utils.find_elements_by_css_selector(driver, 'div.detail-chose-box > div > strong')
        if len(elements) >= 2:
            product['code'] = elements[0].text.strip()
            product['price_cny'] = int(float(elements[1].text.strip()))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.frabic-detail-left > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'table.detail > tbody > tr > td > span.detail')
        product['detail'] = element.text.strip()
        return product