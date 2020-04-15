import json
import sys
import traceback
import urllib.parse
from datetime import datetime
sys.path.append('.')
import of_config
import of_database
import of_utils
import of_errors
from retry import retry
import time

class Spider:
    def __init__(self, logger):
        self.logger = logger
    
    
    def proc(self, brand, source_id, pid, url):
        try:
            try:
                result = self.get_product(brand,source_id,pid,url)
                status = of_config.status_finished
            except Exception as e:
                result = traceback.format_exc()
                status = of_config.status_failed
            self.write_products(brand, url, source_id, pid, status, result)
        except Exception as e:
            self.logger.exception(traceback.format_exc())
            print(e)

    @retry(of_errors.ImagesError,tries=3,delay=2,jitter=1)
    def get_product(self, brand, source_id, pid, url):
        try:
            print ('get_product', int(time.time()))
            driver = None
            driver = of_utils.create_chrome_driver()
            driver.get(url)
            if pid == -1: # entry
                return self.parse_entry(driver)
            else: # product
                return self.parse_product(driver)
        finally:
            driver.quit()

    def write_products(self, brand, url, source_id, pid, status, result):
        if pid == -1: # entry
            if status == of_config.status_finished:
                for product_url in result:
                    product_url = urllib.parse.unquote(product_url)
                    rows = of_database.Source.select().where(of_database.Source.url == product_url)
                    if rows:
                        r = rows.get()
                        r.updated_at = datetime.now()
                    else:
                        r = of_database.Source()
                        r.brand = brand
                        r.url = product_url
                        r.status = of_config.status_new # 新写入，等待解析具体内容。
                    r.pid = source_id # 强制更新
                    r.save()
            r = of_database.Source.select().where(of_database.Source.url == url).get()
            r.status = status
            r.updated_at = datetime.now()
            if status == of_config.status_failed:
                r.message = result
            r.save()
        else: # product
            rows = of_database.Source.select().where(of_database.Source.url == url)
            if rows:
                r = rows.get()
            else:
                r = of_database.Source()
            r.status = status
            r.updated_at = datetime.now()
            r.pid = pid
            if status == of_config.status_finished:
                r.title = result['title']
                r.code = result['code']
                r.price_cny = result['price_cny']
                r.price_euro_de = result['price_euro_de']
                r.price_euro_fr = result['price_euro_fr']
                r.price_euro_ita = result['price_euro_ita']
                r.price_gbp = result['price_gbp']
                r.price_jpy = result['price_jpy']
                r.price_usd = result['price_usd']
                r.price_hkd = result['price_hkd']
                r.images = result['images']
                r.detail = result['detail']
            else: # status_failed
                r.message = result
            r.save()
                
empty_product = {'title': '',
                 'code': '',
                 'price_cny': 0,
                 'price_euro_de': 0,
                 'price_euro_fr': 0,
                 'price_euro_ita': 0,
                 'price_gbp': 0,
                 'price_hkd': 0,
                 'price_jpy': 0,
                 'price_usd': 0,
                 'images': '',
                 'detail': ''}