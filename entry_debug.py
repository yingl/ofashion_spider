import sys
import traceback
sys.path.append('.')
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

def parse_entry(driver):
        product_count = 0
        while True:
            elements = of_utils.find_elements_by_css_selector(driver, 'div.listingItem>a')
            if len(elements) > product_count:
                product_count = len(elements)
                action = ActionChains(driver).move_to_element(elements[-1])
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.send_keys(Keys.PAGE_DOWN)
                action.perform()
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
        driver.get('https://www.tods.cn/cn-zh/%E5%A5%B3/%E5%8C%85%E8%A2%8B/%E6%89%98%E7%89%B9%E6%89%8B%E8%A2%8B/c/123-Tods/')
        products = parse_entry(driver)
        print(products)
        print(len(products))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        if driver:
            driver.quit()
