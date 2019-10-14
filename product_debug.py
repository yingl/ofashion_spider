import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils


def parse_product(driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, "meta[name=keywords]")
        if element:
            product['title'] = element.get_attribute('content').strip().split('，')[0]
        else:
            raise Exception('Title not found')    
        # code
        element = of_utils.find_element_by_css_selector(driver,"meta[property='og:title']")
        if element:
            product['code'] = element.get_attribute('content').strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product-info-price span.price')
        if element:
            product['price_cny'] = of_utils.convert_price(element.text.strip())
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'img.fotorama__img')
        if elements:
            images = [element.get_attribute('src').strip() for element in elements]
        else:
            elements = of_utils.find_elements_by_css_selector(driver, 'ul.newpdp-gallery-slider > li > img')
            images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        return product
if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://www.longines.cn/watch-heritage-l2-813-4-66-0')
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
