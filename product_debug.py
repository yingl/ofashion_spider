import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils
import re

def parse_product(driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, '.product-full__subline')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, '.product-full__content .product-sku-price__value')
        if element:
            product['price_cny'] =  of_utils.convert_price(element.text.strip())
        # # images
        elements = of_utils.find_elements_by_css_selector(driver, '.product-full__image-carousel .product-full__carousel__slides .product-full__carousel__slide img')
        images = ['https://www.lamer.com.cn'+element.get_attribute('data-src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # # detail
        element = of_utils.find_element_by_css_selector(driver, '.product-full__description .product-full__accordion__panel')
        if element:
            product['detail'] = element.text.strip()
        return product

if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        driver.get('https://www.lamer.com.cn/product/5834/12343/creme-de-la-mer/creme-de-la-mer/moisturizer-for-dry-skin')
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
