import sys
import traceback
sys.path.append('.')
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

def parse_entry(driver):
        elements = of_utils.find_elements_by_css_selector(driver, '.product-list ul li a')
        return [element.get_attribute('href').strip() for element in elements if 'tmall' not in element.get_attribute('href').strip()]

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
        driver.get('https://www.lorealparis.com.cn/SkinCare/Franchise/GrapeSeedSeries.loreal')
        products = parse_entry(driver)
        print(products)
        print(len(products))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        if driver:
            driver.quit()
