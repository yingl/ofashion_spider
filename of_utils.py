import importlib
import inspect
import logging
import os
import sys
import time
import traceback
from datetime import datetime
from selenium import webdriver
sys.path.append('.')
import of_spider

def sleep(seconds):
    time.sleep(seconds)

def create_chrome_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    return driver

def find_element_by_css_selector(element, selector):
    try:
        return element.find_element_by_css_selector(selector)
    except:
        return None

def find_elements_by_css_selector(element, selector):
    try:
        return element.find_elements_by_css_selector(selector)
    except:
        return []
   
def create_flogger(filename, level=logging.INFO):
    logger = logging.getLogger(filename)
    logger.setLevel(level)
    dt = datetime.now()
    fh = logging.FileHandler(filename + '_' + dt.strftime('%Y-%m-%d') + '_' + str(os.getpid()) + '.log')
    fh.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

def get_domain(url):
    return url.split('://')[1].split('/')[0]

def load_spiders(path, logger):
    spiders = {}
    files = os.listdir(path)
    for f in files:
        f_path = os.path.join(path, f)
        if os.path.isfile(f_path) and \
           (not f.startswith('__init__')) and \
           f.endswith('.py'):
            mod = importlib.import_module('%s.%s' % (path, f[:-3]))
            for var in dir(mod):
                obj = getattr(mod, var)
                try:
                    if issubclass(obj, of_spider.Spider):
                        var = var.lower()
                        spiders[var] = obj(logger)
                except:
                    pass
    return spiders

def get_base_url(url):
    return url.split('?')[0]

def get_url_parameters(url):
    parameters = {}
    kvs = url.split('?')[-1].split('&')
    for kv in kvs:
        k, v = kv.split('=')
        parameters[k] = v
    return parameters

def convert_price(price):
    try:
        return int(float(price))
    except:
        return 0
