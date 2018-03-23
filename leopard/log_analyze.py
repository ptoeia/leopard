#coding:utf-8
import time
import re
from datetime import datetime


def log_analyze():
    log = '2018-01-21 13:25:08 UTC:172.31.23.33(48935)'\
          ':root@web:[11159]:LOG:  duration: 6156.786 ms  statement: SELECT id,write_date FROM product_product'
    data = {}
    timestamp = re.search('\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\sUTC',log).group()
    ip = re.search('(\d{1,}\.){3}\d{1,}',log).group()
    user = log.split(':')[4]
    duration = log.split(':')[-2].split(' ')[1]
    statement = log.split(':')[-1]
    data['timestamp']=timestamp
    data['ip']=ip
    data['user']=user
    data['duration']=duration
    data['statement']=statement
    for k,v in data.items():
         print k,v
log_analyze()
