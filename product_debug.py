import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils

def parse_product(driver):
    driver.implicitly_wait(15)
    product = of_spider.empty_product.copy()
    # title
    element = of_utils.find_element_by_css_selector(driver, 'div.product-main-bloc > div > div > h1')
    if element:
        product['title'] = element.text.strip()
    else:
        raise Exception('Title not found')
    # code N/A
    element = of_utils.find_element_by_css_selector(driver, 'p.reference > span')
    if element:
        product['code'] = element.text.strip()
    # price_cny N/A
    # images
    elements = of_utils.find_elements_by_css_selector(driver, 'div.product-media > img')
    images = [element.get_attribute('src').strip() for element in elements]
    product['images'] = ';'.join(images)
    # detail
    texts = []
    element = of_utils.find_element_by_css_selector(driver, 'p.shortDescription')
    texts.append(element.get_attribute('innerHTML').strip())
    element = of_utils.find_element_by_css_selector(driver, 'div.box-collateral > p')
    texts.append(element.get_attribute('innerHTML').strip())
    product['detail'] = '\n'.join(texts)
    return product

if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://cn.boucheron.com/zh_cn/the-creations/jewelry/rings/flocon-ring-diamond-mother-of-pearl-white-gold.html')
        product = parse_product(driver)
        print(product)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        if driver:
            driver.quit()
