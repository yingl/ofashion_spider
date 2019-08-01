import sys
import traceback
sys.path.append('.')
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

def parse_entry(driver):
        view_all = of_utils.find_element_by_css_selector(driver, 'span.js-view-all-products')
        if view_all:
            driver.execute_script('arguments[0].click();', view_all)
            of_utils.sleep(3)
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.product-tile > figure.product-image > a.thumb-link')
            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                of_utils.sleep(4)
            else:
                break
        return [element.get_attribute('href').strip() for element in elements]
        # of_utils.sleep(10)
        # elements = of_utils.find_elements_by_css_selector(driver,'.rlxr-watchgrid__watch-list-item>a')
        # return [element.get_attribute('href').strip() for element in elements]

        # product_count = 0
        # while True:
        #     elements = of_utils.find_elements_by_css_selector(driver, 'ul.product-roll-ul > li.search-result > div > div > article > a')
        #     if len(elements) > product_count:
        #         product_count = len(elements)
        #         driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
        #         of_utils.sleep(4)
        #     else:
        #         break
        # return [element.get_attribute('href').strip() for element in elements]

if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://www.loewe.com/chn/zh_CN/%E7%94%B7%E5%A3%AB%E7%B3%BB%E5%88%97/%E6%97%B6%E5%B0%9A%E9%85%8D%E9%A5%B0/%E8%83%B8%E9%92%88	')
        products = parse_entry(driver)
        print(products)
        print(len(products))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        if driver:
            driver.quit()
