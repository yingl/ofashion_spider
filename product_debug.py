import sys
import traceback
sys.path.append('.')
import of_spider
import of_utils
import re
import json
from urllib.request import urlopen
from json import load
from selenium.webdriver.common.action_chains import ActionChains # 对该页面特别处理
from selenium.webdriver.common.keys import Keys

def parse_product(driver):
        driver.implicitly_wait(15)
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_xpath(driver, '//div[@id="productInfoDiv"]//span[@class="dbj-font-header2"]')
        if element:
            product['title'] = element.get_attribute('innerHTML')
        else:
            raise Exception('Title not found')
        # code
        element = of_utils.find_element_by_xpath(driver, '//p[@class="dbj-font-caption1-alt1 pb-1 dbj-border-top"]/span')
        if element:
            product['code'] = element.get_attribute('innerHTML').replace('&nbsp;','')
        # price_cny
        element = of_utils.find_element_by_xpath(driver, '//div[@id="productInfoDiv"]//span[@class="dbj-font-header6 product-price"]')
        if element:
            product['price_cny'] = of_utils.convert_price(element.get_attribute('innerHTML'))
        # images
        elements = of_utils.find_elements_by_xpath(driver, '//div[@class="zoom-trap"]/img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_xpath(driver, '//div[@id="pdpDesktopSlot1"]//p[@class="dbj-font-body1"]')
        if element:
            product['detail'] = element.text.strip()
        return product

if __name__ == '__main__':
    driver = None
    try:
        # ip = urlopen('http://ip.42.pl/raw').read()
        # print(ip)
        driver = of_utils.create_chrome_driver()
        driver.get('https://www.debeers.com.cn/zh-cn/horizon-full-pav%C3%A9-band-in-white-gold/R102281.html')
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
    # import json
    # a = '{"@context":"http://schema.org","@type":"Product","name":"\u5e93\u514b\u8239\u957f\u81ea\u52a8\u673a\u68b0\u8155\u8868","brand":"Rado","image":"https://www.rado.cn/sites/default/files/images/swp/tradition/tradition/r32500315_s.png","description":"\u627f\u88ad1962\u5e74\u7684\u7ecf\u5178\u8bbe\u8ba1\uff0c\u4ee521\u4e16\u7eaa\u5168\u65b0\u59ff\u6001\uff0c\u6f14\u7ece\u7a81\u7834\u6027\u7684\u8bbe\u8ba1\u7406\u5ff5\u3002\u5e93\u514b\u8239\u957f\u8155\u8868\u5728\u590d\u53e4\u7ec6\u8282\u4e2d\u878d\u5165\u524d\u77bb\u6027\u7684\u8bbe\u8ba1\u7406\u5ff5\uff0c\u5168\u65b0\u6f14\u7ece\u4e4b\u4e0b\u4f7f\u8be5\u6b3e\u8155\u8868\u65e0\u60e7\u5c81\u6708\u7684\u8003\u9a8c\uff0c\u662f\u5f53\u4ee3\u4f69\u6234\u8005\u7684\u7ecf\u5178\u4e4b\u9009\u3002","sku":"01.763.0500.3.131","offers":{"@type":"Offer","url":"https://www.rado.cn/collections/tradition/tradition/R32500315","priceCurrency":" CNY","price":"16400","itemCondition":"https://schema.org/NewCondition"}}'
    # b = json.loads(a)
    # print(b['offers']['price'])


    # a = '//player.louisvuitton.com/media/img/poster/video/640x1280/1324/1324007.jpg 1600w,//player.louisvuitton.com/media/img/poster/video/640x1280/1324/1324007.jpg 1280w,//player.louisvuitton.com/media/img/poster/video/640x1280/1324/1324007.jpg 1024w,//player.louisvuitton.com/media/img/poster/video/640x1280/1324/1324007.jpg 640w,//player.louisvuitton.com/media/img/poster/video/640x1280/1324/1324007.jpg 480w,//player.louisvuitton.com/media/img/poster/video/320x640/1324/1324007.jpg 320w,//player.louisvuitton.com/media/img/poster/video/320x640/1324/1324007.jpg 240w'

    # b = a.split(',')[0].replace(' 1600w','').replace(' 1280w','').replace(' 1024w','').replace(' 640w','').replace(' 480w','').replace(' 320w','').replace(' 240w','')
    # print(b)

    # a = '饰26颗珍珠母贝纽扣（可解开前几个纽扣穿着）<br><br>颜色：beige &amp; purple<br>商品编号：CHC20URO3233095U'
    # b = a.find('商品编号33')
    # c = a[a.find('商品编号33')+5:] if a.find('商品编号33') >= 0 else ''
    # print(b)