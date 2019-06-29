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
    products = []
    elements = of_utils.find_elements_by_css_selector(driver, 'ul.product-list > li > div.img-box > a#product_detail_a')
    for element in elements:
        txt = element.get_attribute('name').strip()
        txt = txt.replace('\n', '')
        txt = txt.replace('\t', '')
        products.append('https://china.coach.com' + txt)
    return products

if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://china.coach.com/women/newarrivals.htm?nav=09900100100')
        products = parse_entry(driver)
        print(products)
        print(len(products))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        if driver:
            driver.quit()
