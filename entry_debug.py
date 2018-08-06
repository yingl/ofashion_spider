import sys
sys.path.append('.')
import of_utils

def parse_entry(driver):
    elements = of_utils.find_elements_by_css_selector(driver, 'div.products-list > div > a')
    return [element.get_attribute('href').strip() for element in elements]

if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://cn.boucheron.com/zh_cn/the-creations/watches/quartz.html')
        products = parse_entry(driver)
        print(products)
        print(len(products))
    except:
        pass
    finally:
        if driver:
            driver.quit()
