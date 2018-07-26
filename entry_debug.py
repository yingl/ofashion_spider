import sys
sys.path.append('.')
import of_utils

def parse_entry(driver):
    product_count = 0
    while True:
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.product-roll-ul > li.search-result > div > div > article > a')
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
        driver.get('https://cn.vancleefarpels.com/cn/zh/search/search.html?srchTags=&srchSecondary=CREATIONS&srchText=&isAvail=false&prodSort=&tokenNumber=0.01105722667895459')
        products = parse_entry(driver)
        print(products)
    except:
        pass
    finally:
        if driver:
            driver.quit()
