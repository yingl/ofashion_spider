import sys
import traceback
sys.path.append('.')
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import json

def parse_entry(driver):
        # while True:
        #     btn = of_utils.find_element_by_css_selector(driver,'.paging_tab_loadmore')
        #     if btn:
        #         driver.execute_script('arguments[0].click();', btn)
        #         of_utils.sleep(4)
        #     else:
        #         break    
      
        # elements = of_utils.find_elements_by_css_selector(driver, "ul.products>li>a") 
        # return [element.get_attribute('href').strip() for element in elements]  

        # of_utils.sleep(4)
        # product_count = 0
        # while True:
        #     elements = of_utils.find_elements_by_css_selector(driver, '#siteContent ul li a')
        #     if len(elements) > product_count:
        #         product_count = len(elements)
        #         action = ActionChains(driver).move_to_element(elements[-1])
        #         action.send_keys(Keys.PAGE_DOWN)
        #         action.send_keys(Keys.PAGE_DOWN)
        #         action.send_keys(Keys.PAGE_DOWN)
        #         action.send_keys(Keys.PAGE_DOWN)
        #         action.send_keys(Keys.PAGE_DOWN)
        #         action.perform()
        #         of_utils.sleep(4)
        #     else:
        #         break
        # return [element.get_attribute('href').strip() for element in elements]

        # elements = of_utils.find_elements_by_css_selector(driver, "article>div>a") 
        # return [element.get_attribute('href').strip() for element in elements]  

        # urls = []
        # while True:
        #     elements = of_utils.find_elements_by_css_selector(driver, 'ul.products-grid>li>div>a ')
        #     if elements:
        #         for ele in elements:
        #             urls.append(ele.get_attribute('href').strip())
        #     btn = of_utils.find_element_by_css_selector(driver,'.toolbar-bottom .pager .pages .i-next')
        #     if btn:
        #         driver.execute_script('arguments[0].click();', btn)
        #         of_utils.sleep(4)
        #     else:    
        #         break
        # return urls

        # product_count = 0
        # while True:
        #     elements = of_utils.find_elements_by_css_selector(driver, '.product_listing_container ul li a')
        #     if len(elements) > product_count:
        #         product_count = len(elements)
        #         action = ActionChains(driver).move_to_element(elements[-1])
        #         action.send_keys(Keys.PAGE_DOWN)
        #         action.send_keys(Keys.PAGE_DOWN)
        #         action.send_keys(Keys.PAGE_DOWN)
        #         action.send_keys(Keys.PAGE_DOWN)
        #         action.send_keys(Keys.PAGE_DOWN)
        #         action.perform()
        #         of_utils.sleep(4)
        #     else:
        #         break
        # return [element.get_attribute('href').strip() for element in elements]
        # supreme
        # elements = of_utils.find_elements_by_css_selector(driver, '#shop-scroller > li > a')
        # return [element.get_attribute('href').strip() for element in elements]  

        driver.implicitly_wait(15)
        elements = of_utils.find_elements_by_xpath(driver, '//a[@class="pdp-link image-link"]')
        return [element.get_attribute('href').strip() for element in elements]

if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://www.sergiorossi.com/cn-en/shoes/boots/')
        products = parse_entry(driver)
        print(products)
        print(len(products))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        if driver:
            driver.quit()
