import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils


def parse_product(driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'article.product-details h1.product-details_name')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product-details_price>span')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product-details-main-information_media>picture>img')
        if not elements:
            elements = of_utils.find_elements_by_css_selector(driver,'.product-details_images>picture>img')
        images = [element.get_attribute('src') if element.get_attribute('src') else 'https://www.alexanderwang.cn'+element.get_attribute('data-src')  for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, '.product-details-description>div>div')
        if element:
            product['detail'] = element.text.strip()
        return product
        
if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://www.alexanderwang.cn/cn-zh/lyndon-halo-boot+887032838609.html')
        product = parse_product(driver)
        print(product)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        if driver:
            driver.quit()
