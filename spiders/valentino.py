import sys
sys.path.append('../')
import of_spider
import of_utils

class Valentino(of_spider.Spider):
    def parse_entry(self, driver):
        while True:
            btn = of_utils.find_element_by_css_selector(driver, 'button.loadMoreProductsButton ')
            if btn:
                if btn.get_attribute('disabled') == None:
                    break
                else:
                    driver.execute_script('arguments[0].click();', btn)
                    of_utils.sleep(2)
            else:
                break
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.products > li.searchresult__item > figure > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.item-name > span.modelName')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.modelfabricolor > p > span.value')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.itemPrice > span.price > span.value')
        if element:
            price_text = element.text.strip().replace(',', '')
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '#leftPart > div.imagesContent.productShots > div.alternativeDots.productShots__gallery.productShots__gallery--alternative > div > ul > li > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'p.attributes.editorialdescription > span.value')
        product['detail'] = element.text.strip()
        return product