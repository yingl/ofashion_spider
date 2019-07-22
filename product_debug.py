import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils


def parse_product(driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div#productName > h1')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'div#infoProductBlock h1#productName')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'div.sku')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'span.sku')
        if element:
            product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'td.priceValue')
        if not element:
            element =  of_utils.find_element_by_css_selector(driver, 'div#infoProductBlock div.priceBlock div.priceValue')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.thumbnails ul li picture source')
        if not elements:
            elements = of_utils.find_elements_by_css_selector(driver, '#productMainImage source')  
        images = [element.get_attribute('srcset').strip().split(',')[0] for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'div.productDescription[itemprop=description]')
        if not element:
            element = of_utils.find_element_by_css_selector(driver, 'div#productDescription')
        if element:
            product['detail'] = element.text.strip()
        return product
        
if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://www.louisvuitton.cn/zhs-cn/products/avenue-sling-bag-damier-infini-nvprod1300037v')
        product = parse_product(driver)
        print(product)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        if driver:
            driver.quit()
