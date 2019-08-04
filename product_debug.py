import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils


def parse_product(driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, "meta[property='og:title']")
        if element:
            product['title'] = element.get_attribute('content').strip().replace('"','')
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver,'.secondary-info .p-secondary')
        if element:
             product['code'] = element.text.strip()
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.product-images>div>img')
        if elements:
            images = [element.get_attribute('src').strip() for element in elements]
            product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver,'#description-tab')
        if element:
            product['detail'] = element.text.strip()
        return product

if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://cn.maxmara.com/p-9226219906002-domez-dark-bown')
        product = parse_product(driver)
        print(product)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        if driver:
            driver.quit()
