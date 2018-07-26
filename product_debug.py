import sys
sys.path.append('.')
import of_spider
import of_utils

def parse_product(driver):
    product = of_spider.empty_product.copy()
    # title
    element = of_utils.find_element_by_css_selector(driver, 'div.product-info > h1.name')
    if element:
        product['title'] = element.text.strip()
    else:
        raise Exception('Title not found')
    # code
    element = of_utils.find_element_by_css_selector(driver, 'p.productreference > span.productreference-value')
    if element:
        product['code'] = element.text.strip()
    # price_cny
    element = of_utils.find_element_by_css_selector(driver, 'span.price.price-details')
    if element:
        price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
        product['price_cny'] = int(float(price_text))
    # images
    elements = of_utils.find_elements_by_css_selector(driver, 'div.slick-track > div.big-picture > img')
    images = [element.get_attribute('src').strip() for element in elements]
    product['images'] = ';'.join(images)
    # detail
    element = of_utils.find_element_by_css_selector(driver, 'div.VCA-product-details_description-ct > p')
    product['detail'] = element.text.strip()
    return product

if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://cn.vancleefarpels.com/cn/zh/collections/jewelry/alhambra/magic-alhambra/vcarn5jr00-magic-alhambra-earclips-2-motifs.html')
        product = parse_product(driver)
        print(product)
    except:
        pass
    finally:
        if driver:
            driver.quit()
