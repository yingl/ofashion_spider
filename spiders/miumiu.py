import sys
sys.path.append('../')
import of_spider
import of_utils

class MiuMiu(of_spider.Spider):
    def parse_entry(self, driver):
        while True:
            btns = of_utils.find_elements_by_css_selector(driver, '.collapse-link-container>a')
            if btns:
                for btn in btns:
                    driver.execute_script('arguments[0].click();', btn)
                    of_utils.sleep(2)
            else:
                break

        elements = of_utils.find_elements_by_css_selector(driver, 'div.nextCategory>div>a')
        driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.infos .nameProduct')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.shop-content .yourSelectionCode')
        if element:
            product['code'] = element.text.strip().replace('产品：','')
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.shop-content span.price')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.mainImageSlider-nav li>img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        return product