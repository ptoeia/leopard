#!/usr/bin/env python
#-*- coding:utf-8 -*-
from alarminit import AlarmBase
import sys
import boto3

client = boto3.client('cloudwatch')

# 实例的内存、带宽大小
redis_hardware_info = { 
    'cache.r3.large' :[
         {'memory': 13.5, 'network': 0.5}
         ] ,
    'cache.m4.large' :[
         {'memory': 6, 'network': 0.5}
         ] ,
    'cache.m4.xlarge' :[
         {'memory': 14, 'network': 1}
         ],
    'cache.m4.2xlarge' :[
         {'memory': 30, 'network': 1}
         ],
    'cache.r4.large' :[
         {'memory': 12.3, 'network': 10}
         ],
    'cache.r4.xlarge' :[
         {'memory': 25, 'network': 10}
         ],
    'cache.m4.2xlarge' :[
         {'memory': 30, 'network': 1}
         ]

}

class AlarmBase(object):

    __init__(self):
        self.client = boto3.client('cloudwatch')



    def create_alrm(self,**kwargs):
        self.put_metric_alarm(**kwargs)

class redis_alarm(AlarmBase):

    def _get_hardware_size(self, CacheClusterd):
        '''
         :params CacheClusterId = CacheNodeId
          
        return cache instance's networkbandwidth
          根据实例类型返回实例的
          最大带宽
          最大内存
        '''  
        client = boto3.client('elasticache')
        response = client.describe_cache_clusters(
            CacheClusterId=CacheClusterd
        )
        try:
            CacheNodeType = response['CacheClusters'][0]['CacheNodeType']
            memory_size = redis_hardware_info.get(CacheNodeType)[0]['memory']
            network_bandwidth = redis_hardware_info.get(CacheNodeType)[0]['network'] 
            return (int(memory_size), int(network_bandwidth))    
        except Exception as e:
            print('不存在此实例硬件信息') 
            sys.exit(1)
    
    def create_networkout_alarm(CacheClusterId,CacheNodeId='0001'): 
        client.put_metric_alarm(
            AlarmName = 'Redis-{}-NetworkBytesOut'.format(CacheClusterId),
            AlarmDescription = 'NetworkBytesOut exceed 90% of Max',
            ActionsEnabled = True,
            #OKActions = [ ACTION_SNS_TOPIC,],
            OKActions = cls.OKActions,
            AlarmActions = cls.AlarmActions,
            MetricName = 'NetworkBytesOut',
            Namespace = 'AWS/ElastiCache',
            Statistic = 'Maximum',
            Dimensions = [
                {
                     "Name": "CacheClusterId", 
                     "Value": CacheClusterId
                }, 
                {
                    "Name": "CacheNodeId", 
                    "Value": CacheNodeId 
                }
                ], 
    
           Period = cls.Period,
           #Unit = 'Percent',
           EvaluationPeriods = 3,
           Threshold = int(  # 阈值为实例网络输出每分钟的字节数x90%
                           _get_hardware_size(CacheClusterId)[-1]
                           *pow(1024,3)*60/8*0.9
                       ),  
           ComparisonOperator = 'GreaterThanThreshold'
           )
    
    def create_memory_alarm(CacheClusterd, CacheNodeId='0001'): 
        PERIOD_IN_SECONDS = 300
        client.put_metric_alarm(
            AlarmName = 'Redis-{}-Low-FreeableMemory'.format(CacheClusterd),
            AlarmDescription = 'FreeableMemory less than 20%',
            ActionsEnabled = True,
            OKActions = [ ACTION_SNS_TOPIC,],
            AlarmActions = [ ACTION_SNS_TOPIC,],
            MetricName = 'FreeableMemory',
            Namespace = 'AWS/ElastiCache',
            Statistic = 'Average',
            Dimensions = [
                {
                     "Name": "CacheClusterId", 
                     "Value": CacheClusterd
                }, 
                {
                     "Name": "CacheNodeId", 
                     "Value": CacheNodeId 
                }
                ], 
           Period = PERIOD_IN_SECONDS,
           #Unit = 'Percent',
           EvaluationPeriods = 1,
           Threshold = int(
                           _get_hardware_size(CacheClusterd)[0]
                           *pow(1024,3)*0.2
                          ),  
           ComparisonOperator = 'LessThanThreshold'
           )
    
    def create_cpu_alarm(CacheCluterId,CacheNodeId='0001'): 
        ACTION_SNS_TOPIC = 'arn:aws:sns:us-west-2:660338696248:CloudWatchAlarm'
        PERIOD_IN_SECONDS = 300
        client.put_metric_alarm(
            AlarmName = 'Redis-{}-High-cpu'.format(CacheCluterId),
            AlarmDescription = 'cpu util more than 80%',
            ActionsEnabled = True,
            #OKActions = [ ACTION_SNS_TOPIC,],
            AlarmActions = [ ACTION_SNS_TOPIC,],
            MetricName = 'EngineCPUUtilization', 
            Namespace = 'AWS/ElastiCache',
            Statistic = 'Average',
            Dimensions = [
                {
                    "Name": "CacheClusterId", 
                    "Value": CacheCluterId
                }, 
                {
                    "Name": "CacheNodeId", 
                    "Value": CacheNodeId 
                }
            ], 
            Period = PERIOD_IN_SECONDS,
            #Unit = 'Percent',
            EvaluationPeriods = 1,
            Threshold = 80,
            ComparisonOperator = 'GreaterThanThreshold'
            )
    
    def create_swap_alarm(CacheClusterId, CacheNodeId='0001'): 
        ACTION_SNS_TOPIC = 'arn:aws:sns:us-west-2:660338696248:CloudWatchAlarm'
        PERIOD_IN_SECONDS = 300
        client.put_metric_alarm(
            AlarmName = 'Redis-{}-High-swap'.format(CacheClusterId),
            AlarmDescription = 'swap more than 50M',
            ActionsEnabled = True,
            #OKActions = [ ACTION_SNS_TOPIC,],
            AlarmActions = [ ACTION_SNS_TOPIC,],
            MetricName = 'SwapUsage',
            Namespace = 'AWS/ElastiCache',
            Statistic = 'Average',
            Dimensions = [
                    {
                        "Name": "CacheClusterId", 
                        "Value": CacheClusterId
                    }, 
                    {
                        "Name": "CacheNodeId", 
                        "Value": CacheNodeId
                    }
                ], 
    
           Period = PERIOD_IN_SECONDS,
           #Unit = 'Percent',
           EvaluationPeriods = 1,
           Threshold = 50*pow(1024,2),   #阈值为50M
           ComparisonOperator = 'GreaterThanThreshold'
           )
    
    def main(CacheClusterId):    
        try:
            create_networkout_alarm(CacheCluterId)
            create_memory_alarm(CacheCluterId)
            create_cpu_alarm(CacheCluterId) 
            create_swap_alarm(CacheCluterId) 
            print "add alarm success"
        except Exception,e:
            print(e)
