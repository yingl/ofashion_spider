import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils


def parse_product(driver):
        product = of_spider.empty_product.copy()

        ele = of_utils.find_element_by_css_selector(driver, 'div.product-name>h1')
        product['title'] = ele.text.strip() if ele else ''

        ele = of_utils.find_element_by_css_selector(driver, 'div[itemprop=sku]')
        product['code'] = ele.text.strip() if ele else ''        

        ele = of_utils.find_element_by_css_selector(driver, 'meta[itemprop=price]')
        product['price_cny'] = of_utils.convert_price(ele.get_attribute('content').strip()) if ele else 0

        # images
        imgs=[]
        eles = of_utils.find_elements_by_css_selector(driver, '.fotorama__thumb>img')
        for ele in eles:
            img = ele.get_attribute('src').strip().replace('cache', '')
            for a in img.split('/'):
                if len(a) == 32:
                    img = img.replace(a,'')
            imgs.append(img)    
        product['images'] = ';'.join(imgs)

        return product

if __name__ == '__main__':
    driver = None
    try:
        driver = of_utils.create_chrome_driver()
        # driver.get('https://www.bulgari.cn/zh-cn/jewelry/rings/bzero1/an856221.html')
        driver.get('https://www.bulgari.cn/zh-cn/an191025.html')
        product = parse_product(driver)
        print(product)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        if driver:
            driver.quit()
