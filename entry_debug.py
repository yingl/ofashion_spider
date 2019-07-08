import sys
import traceback
sys.path.append('.')
import of_utils
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

def parse_entry(driver):
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
                else:
                    break
            else:
                break
        return urls

if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://cn.iteshop.com/b_it/women/new-arrivals?page=1&fo=ct&ct=5&customizeConditionsType=WOMEN_NEW_ARRIVALS')
        products = parse_entry(driver)
        print(products)
        print(len(products))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        if driver:
            driver.quit()
