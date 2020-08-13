import argparse
import importlib
import sys
import traceback
sys.path.append('.')
import of_config
import of_database
import of_queue
import of_utils
import json

logger = of_utils.create_flogger(__file__)

def parse_args(config='of_config'):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--config',
                        type=str,
                        default=config)
    return parser.parse_args()

def loop(config):
    of_database.init_database(config.db)
    spiders = of_utils.load_spiders(config.spiders, logger)
    rqueue = of_queue.Queue(config.rqueue)
    mapping = config.mapping
    '''
    jobs = [{'source_id': 200, 
                'pid': 100,
                'url': "http://store.tods.cn/Tods/CN/Tod's-Wave-迷你牛皮背包/p/XBWAMRGD101MCAL020"}] # Mock fetch a job
    for job in jobs:
    '''
    while True:
        try:
            r = rqueue.get()
            print(r)
            job = eval(r)    
            url = job['url']
            domain = of_utils.get_domain(url)
            brand = mapping[domain]
            spider = spiders[brand]
            spider.proc(brand, job['source_id'], job['pid'], url)
        except Exception as e:
            logger.exception(traceback.format_exc())

# def test(config):
#     of_database.init_database(config.db)
#     spiders = of_utils.load_spiders(config.spiders, logger)
#     mapping = config.mapping
#     job = {'source_id': 100370, 
#             'pid': 100333,
#             'url': "https://www.chloe.cn/cn/%E7%9A%AE%E5%A4%B9_cod22005800ob.html"}
#     url = job['url']
#     domain = of_utils.get_domain(url)
#     brand = mapping[domain]
#     spider = spiders[brand]
#     spider.proc(brand, job['source_id'], job['pid'], url)

if __name__ == '__main__':
    # args = parse_args()
    # config = importlib.import_module(args.config)
    # loop(config)
    # test(config)

    a = '{"source_id":226663,"pid":-1,"url":"https://www.debeers.com.cn/zh-cn/jewellery/classics/","spider":null}'.replace('null','')
    b = json.dumps(a)
    c = eval(a)
    print(c['url'])
