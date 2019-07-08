import argparse
import importlib
import sys
import traceback
sys.path.append('.')
import of_config
import of_database
import of_queue
import of_utils

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

if __name__ == '__main__':
    args = parse_args()
    config = importlib.import_module(args.config)
    loop(config)