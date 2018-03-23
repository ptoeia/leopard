#coding:utf-8
#Author:gewuzhang
import boto3
import time
from datetime import datetime


def put_firehose():
    client = boto3.client('firehose')
    date =  datetime.now().strftime('%Y-%m-%d:%H:%M:%S')
    log = '2018-01-21 13:25:08 UTC:172.31.23.33(48935)'\
          ':root@web:[11159]:LOG:  duration: 6156.786 ms  statement: SELECT id,write_date FROM product_product'
    try:
        response = client.put_record(
            DeliveryStreamName = 'app-pg-slowlog',
            Record = { 
                   'Data':log
                   }
          )
        print response['RecordId']
    except Exception as e:
        print "push failed:{}".format(e)

if __name__=='__main__':
    put_firehose()
