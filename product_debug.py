import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils


def parse_product(driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'div.product-card > span')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_css_selector(driver, 'span.reference-jewelry')
        if element:
            product['code'] = element.text.strip()
        # price_cny N/A
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'div.content > img.carousel-slide__media')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        texts = []
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.fiche-details__left > li')
        for element in elements:
            detail = ''
            k_element = of_utils.find_element_by_css_selector(element, 'span')
            v_element = of_utils.find_element_by_css_selector(element, 'p')
            txt = k_element.text.strip() + '：' + v_element.text.strip() if  k_element else v_element.text.strip()
            texts.append(txt)
        product['detail'] = '\n'.join(texts)
        return product
        
if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://www.chaumet.com/zh-hans/high-jewellery/hortensia-collection/jardins-hortensia-voie-lactee-ring-082871')
        product = parse_product(driver)
        print(product)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        if driver:
            driver.quit()
