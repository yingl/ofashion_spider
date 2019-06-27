import sys
import traceback
sys.path.append('.')
import of_utils

def loadmore(driver):
    btns = of_utils.find_elements_by_css_selector(driver, 'button.see-more')
    if btns:
        for btn in btns:
            driver.execute_script('arguments[0].click();', btn)
            of_utils.sleep(2)
        loadmore(driver)    
    else:
        return

def parse_entry(driver):
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

if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://www.bulgari.cn/zh-cn/jewellery/rings.html')
        products = parse_entry(driver)
        print(products)
        print(len(products))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        if driver:
            driver.quit()
