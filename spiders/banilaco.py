import sys
sys.path.append('../')
import of_spider
import of_utils

class Banilaco(of_spider.Spider):
    def parse_entry(self, driver):
        products = []
        base_url = of_utils.get_base_url(driver.current_url)
        parameters = of_utils.get_url_parameters(driver.current_url)
        val_bancd = parameters['banCd']
        products = []
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.pdtList > li.pdtItem > div.pdtWrap > a')
        for element in elements:
            s = element.get_attribute('onclick')
            s = s.split('(')[-1].split(')')[0].strip()
            url = 'http://www.banilaco.com.cn/cn/ch/product/productView.do?banCd=' + val_bancd + '&prdSeq=' + s
            products.append(url)
        return products

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.pdtInfo > h2.pdt_tit')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div#visualImg > div.slick-list > div.slick-track > div.item.slick-slide > div.opt_img > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div#pdtInfoTab2')
        product['detail'] = element.text.strip()
        return product