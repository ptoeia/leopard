#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author:gewuzhang

import boto3

client = boto3.client('cloudwatch')
def get_redis_name():
    client = boto3.client('elasticache')
    response = client.describe_cache_clusters()
    s = [each['CacheClusterId'] for each in response['CacheClusters']]
    return  s
        
def create_networkoutbytes_alarm(cache_name,cachenodeid): 
    ACTION_SNS_TOPIC = 'arn:aws:sns:us-west-2:660338696248:CloudWatchAlarm'
    PERIOD_IN_SECONDS = 60
    client.put_metric_alarm(
        AlarmName = 'Redis {} NetworkBytesOut'.format(cache_name),
        AlarmDescription = 'NetworkBytesOut exceed 90% of Max',
        ActionsEnabled = True,
        OKActions = [ ACTION_SNS_TOPIC,],
        AlarmActions = [ ACTION_SNS_TOPIC,],
        MetricName = 'NetworkBytesOut',
        Namespace = 'AWS/ElastiCache',
        Statistic = 'Maximum',
        Dimensions = [
                {
                    "Name": "CacheClusterId", 
                    "Value": cache_name
                }, 
                {
                    "Name": "CacheNodeId", 
                    "Value": cachenodeid 
                }
            ], 

       Period = PERIOD_IN_SECONDS,
       #Unit = 'Percent',
       EvaluationPeriods = 3,
       Threshold = 6000000000,
       ComparisonOperator = 'GreaterThanThreshold'
       )

def create_memory_alarm(cache_name,cachenodeid): 
    ACTION_SNS_TOPIC = 'arn:aws:sns:us-west-2:660338696248:CloudWatchAlarm'
    PERIOD_IN_SECONDS = 300
    client.put_metric_alarm(
        AlarmName = 'Redis-{}-Low-FreeableMemory'.format(cache_name),
        AlarmDescription = 'FreeableMemory less than 2G',
        ActionsEnabled = True,
        OKActions = [ ACTION_SNS_TOPIC,],
        AlarmActions = [ ACTION_SNS_TOPIC,],
        MetricName = 'FreeableMemory',
        Namespace = 'AWS/ElastiCache',
        Statistic = 'Average',
        Dimensions = [
                {
                    "Name": "CacheClusterId", 
                    "Value": cache_name
                }, 
                {
                    "Name": "CacheNodeId", 
                    "Value": cachenodeid 
                }
            ], 

       Period = PERIOD_IN_SECONDS,
       #Unit = 'Percent',
       EvaluationPeriods = 1,
       Threshold = 2000000000,
       ComparisonOperator = 'LessThanThreshold'
       )

if __name__=='__main__':
    #redis_name_list = get_redis_name()
    CacheNodeId_list = ['app-product-2-001', 'app-product-2-002', 'app-product-2-003', 'app-product-2-004', 'app-product-2-006', 'app-product-3-001', 'app-product-3-002'] 
    for CacheNodeId in CacheNoId_list:    
        try:
            create_network_alarm(CacheNodeId,'0001')
            create_memory_alarm(CacheNodeId,'0001')
            print "add alarm success"
        except Exception,e:
            print e
