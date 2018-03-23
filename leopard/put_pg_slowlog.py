#-*-:coding:utf-8 -*-
# push web pg slowlog to elasticsearch  
import boto3
import re
import sys
from datetime import datetime,timedelta

def rds_slowlog_push(rds_instance_id):
    Marker = '0'
    slow_log_list = []
    additionalDataPending = True
    logfile_prefix = 'error/postgresql.log.'
    logfile_name = logfile_prefix+(datetime.now()-timedelta(hours=1)).strftime('%Y-%m-%d-%H')
    client = boto3.client('rds')
    while additionalDataPending:
        response = client.download_db_log_file_portion(
            DBInstanceIdentifier = rds_instance_id, 
            LogFileName = logfile_name, 
            Marker = Marker,
            NumberOfLines = 4000
                        )
        Marker = response['Marker']
        additionalDataPending = response['AdditionalDataPending']
        #p = r'.+LOG:.*duration.*\n(\t{1,}.*\n){0,}'
        p = r'.*duration.*\n(\t{1,}.*\n){0,}'
        try:
            content = re.search(p,response['LogFileData']).group()
            #if content:
            #sns_client = boto3.client('sns')
            #try:
                #message = content.group().replace('\n','')
               # message = content.group()
                #response = sns_client.publish(
                #    TopicArn = 'arn:aws:sns:us-west-2:660338696248:app-pg-slowlog',
                #    Message = message,
                #    Subject = 'App Postgresql SlowLog'
                # )
                #print(datetime.now().strftime('%Y-%m-%H:%M:%S')+' Publish to SNS Channel SNS Message Id:{}'.format(response['MessageId']))
            print(content)
        except Exception as e:
                #pass
            print('no slowlog this time')
            #print(e)
        #else:
        #    print('.......No SlowLog This Time')

rds_slowlog_push('webrdsprod')
