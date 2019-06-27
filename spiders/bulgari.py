import sys
sys.path.append('../')
import of_spider
import of_utils

class Bulgari(of_spider.Spider):
    def loadmore(driver):
        btns = of_utils.find_elements_by_css_selector(driver, 'button.see-more')
        if btns:
            for btn in btns:
                driver.execute_script('arguments[0].click();', btn)
                of_utils.sleep(2)
            loadmore(driver)    
        else:
            return

    def parse_entry(self, driver):
        product_count = 0
        of_utils.sleep(10)
        loadmore(driver)

        while True:
            elements = of_utils.find_elements_by_css_selector(driver, '.product-item-details>div>a')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(4)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()

        ele = of_utils.find_element_by_css_selector(driver, 'div.product-name>h1')
        product['title'] = ele.text.strip() if ele else ''

        ele = of_utils.find_element_by_css_selector(driver, 'div[itemprop=sku]')
        product['code'] = ele.text.strip() if ele else ''        

        ele = of_utils.find_element_by_css_selector(driver, 'meta[itemprop=price]')
        product['price_cny'] = of_utils.convert_price(ele.get_attribute('content').strip()) if ele else 0

        # images
        imgs=[]
        eles = of_utils.find_elements_by_css_selector(driver, '.fotorama__thumb>img')
        for ele in eles:
            img = ele.get_attribute('src').strip().replace('cache', '')
            for a in img.split('/'):
                if len(a) == 32:
                    img = img.replace(a,'')
            imgs.append(img)    
        product['images'] = ';'.join(imgs)

        return product