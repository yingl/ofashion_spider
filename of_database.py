import argparse
import importlib
import inspect
import sys
import traceback
from datetime import datetime
from peewee import BooleanField # peewee相关模块
from peewee import CharField
from peewee import DateTimeField
from peewee import FloatField
from peewee import IntegerField
from peewee import Model
from peewee import MySQLDatabase
from peewee import TextField

class Source(Model):
    url = TextField()
    pid = IntegerField() # -1代表入口页面，其它代表产品页面
    status = CharField()
    message = TextField(default='')
    brand = CharField()
    title = CharField(default='')
    code = CharField(default='')
    price_cny = IntegerField(default=0.0) # 人民币
    price_euro_de = IntegerField(default=0.0) # 德国的欧元报价
    price_euro_fr = IntegerField(default=0.0) # 法国的欧元报价
    price_euro_ita = IntegerField(default=0.0) # 意大利的欧元报价
    price_gbp = IntegerField(default=0.0) # 英镑报价
    price_jpy = IntegerField(default=0.0) # 日元报价
    price_usd = IntegerField(default=0.0) # 美元报价
    price_hkd = IntegerField(default=0.0) # 港币
    images = TextField(default='')
    detail = TextField(default='')
    enabled = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    class Meta:
        database = None

def init_database(config):
    db = MySQLDatabase(host=config['host'],
                       port=config['port'],
                       user=config['user'],
                       password=config['passwd'],
                       database=config['database'],
                       charset=config['charset'])
    # If using the lower version of peewee, uncomment the code to fix this issue: 
    # _mysql_exceptions.OperationalError: (2006, 'MySQL server has gone away')
    # db.get_conn().ping(True)
    for var in dir(sys.modules[__name__]): # Load tables dynamically
        if var != 'Model':
            obj = eval(var)
            if inspect.isclass(obj) and issubclass(obj, Model):
                # About meta programming, refer https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014319106919344c4ef8b1e04c48778bb45796e0335839000
                obj._meta.database = db
    return db

def parse_args(config='of_config'):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--config',
                        type=str,
                        default=config)
    return parser.parse_args()

if __name__ == '__main__':
    database = None
    args = parse_args()
    config = importlib.import_module(args.config)
    try:
        database = init_database(config.db)
        tables = []
        for var in dir(sys.modules[__name__]):
            if var != 'Model':
                obj = eval(var)
                if inspect.isclass(obj) and issubclass(obj, Model):
                    tables.append(obj)
        database.create_tables(tables, safe=True)
    except Exception as e:
        print('%s\n%s' % (e, traceback.print_exc()))
    finally:
        if database:
            database.close()
