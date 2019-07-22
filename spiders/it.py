import sys
sys.path.append('../')
import of_spider
import of_utils

class IT(of_spider.Spider):
    def parse_entry(self, driver):
        urls = []
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, '.list-right-content .list-item .img-box a')
            if elements:
                for ele in elements:
                    if ele.get_attribute('href') != None:
                        urls.append(ele.get_attribute('href').strip())
            
            total_page =  of_utils.find_element_by_css_selector(driver, '#totalPages').get_attribute('value')
            cur_page =  of_utils.find_element_by_css_selector(driver, '#currentPage').get_attribute('value')
            # print('cur:%s,total:%s' % (cur_page,total_page))
            if cur_page != total_page:
                btn = of_utils.find_element_by_css_selector(driver, '.next-page')
                if btn:
                     driver.execute_script('arguments[0].click();', btn)
                     of_utils.sleep(4)
                else:
                    break
            else:
                break
        return urls

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.product-name-pdp>p')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product-price-pdp .product-price-box span')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '#main li.pdp-gallery-list .scroll-background-image a img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        # element = of_utils.find_element_by_css_selector(driver, '.product__info .info__summary')
        # if element:
        #     product['detail'] = element.text.strip()
        return product