import sys
sys.path.append('../')
import of_spider
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

class Annasui(of_spider.Spider):
    def parse_entry(self, driver):
        urls = []
        while True:
            hasNext = False
            elements = of_utils.find_elements_by_css_selector(driver, '#product-loop>div.product>div.ci>a')
            if elements:
                for ele in elements:
                    urls.append(ele.get_attribute('href').strip())

            btns = of_utils.find_elements_by_css_selector(driver,'#pagination a')
            for btn in btns:
                if btn.text.strip() == '>':
                     driver.execute_script('arguments[0].click();', btn)
                     of_utils.sleep(4)
                     hasNext = True   
            if not hasNext:
                break
        return urls

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, "h1[itemprop='name']")
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, "#product-price>span")
        if element:
            product['price_usd'] = int(float(element.text.strip().replace('$','').replace(',','')))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '#product-main-image>img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        return product