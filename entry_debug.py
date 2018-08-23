import sys
import traceback
sys.path.append('.')
import of_utils

def parse_entry(driver):
    elements = of_utils.find_elements_by_css_selector(driver, 'div.product > div.inner > figure > a')
    return [element.get_attribute('href').strip() for element in elements]

if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://www.giuseppezanotti.cn/woman/shoes')
        products = parse_entry(driver)
        print(products)
        print(len(products))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        if driver:
            driver.quit()
