import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils


def parse_product(driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1.page-title>span')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # element = of_utils.find_element_by_css_selector(driver,'.product-sku')
        # if element:
        #     product['code'] = element.text.strip()
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, ".product-info-main .price-final_price .price")
        if element:
            product['price_euro_ita'] = int(float(element.text.strip().replace('£','').replace(',','')))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, '.i-amphtml-slide-item img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail N/A
        # element = of_utils.find_element_by_css_selector(driver,'.watch-info-item>p')
        # if element:
        #     product['detail'] = element.text.strip()
        return product

if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://www.paulsmith.com/uk/men-s-tailored-fit-grey-herringbone-pattern-wool-blazer')
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
