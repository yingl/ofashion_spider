import sys
sys.path.append('../')
import of_spider
import of_utils

class GivenchyBeauty(of_spider.Spider):
    def parse_entry(self, driver):
        elements = of_utils.find_elements_by_css_selector(driver, 'article.giv-ProductTile-item.js-ProductItem > a')
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.giv-ProductDetailHeaderWrapper--desktop .product-name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'span[itemprop=productID]')
        if element:
            product['code'] = element.text.strip()
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.slick-track > a > picture > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.giv-ProductDescription-contentDetail-Detail > div.giv-ProductDescription-contentDetail-Detail-contentText > p')
        product['detail'] = element.get_attribute('innerHTML').strip()
        return product