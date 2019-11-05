import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils
import re

def parse_product(driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.product-template__details .product-details h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product-template__details .product-details__price')
        if element:
            product['price_usd'] = int(float(element.text.strip().replace('$','')))
        # # images
        elements = of_utils.find_elements_by_css_selector(driver, '.product-image-gallery .VueCarousel-inner img')
        if elements:
            images = [element.get_attribute('src').strip() for element in elements]
            product['images'] = ';'.join(images)
        # # detail N/A
        return product

if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://www.victoriabeckhambeauty.com/products/satin-kajal-liner/?variant=black')
        product = parse_product(driver)
        print(product)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        if driver:
            driver.quit()
    # a = 'background-repeat: no-repeat; background-position: center center; width: 75px; height: 75px; background-image: url(&quot;https://hanes.scene7.com/is/image/Hanesbrands/HNS_P0819549316_GraniteHeather?defaultImage=Hanesbrands/HNS_P0819549316_GraniteHeather&amp;layer=comp&amp;fit=constrain,1&amp;wid=75&amp;hei=75&amp;fmt=jpg&amp;resmode=sharp2&amp;op_sharpen=1&quot;);'
    # b = a[a.index('background-image')+28:-3]
    # print(b)
