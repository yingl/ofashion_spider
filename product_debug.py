import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils


def parse_product(driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, ".product-name")
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.price-sales')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.c-block-shopingmodal-main-thumbnail .slick-list .slick-slide img')
        if elements:
            images = [element.get_attribute('src').strip() for element in elements]
            product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver,'.c-block-richcontent-text')
        if element:
            product['detail'] = element.text.strip()
        return product

if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://www.cledepeau-beaute.com.cn/intensive-emulsion-A15401.html?cgid=products-skincare-allproducts')
        product = parse_product(driver)
        print(product)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        if driver:
            driver.quit()
