#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import boto3
from alarminit import AlarmBase 

# aws redis实例的内存、带宽大小
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
         ],
    'cache.t2.medium' :[
         {'memory': 3, 'network': 0.5}
         ]
}
class redis_alarm(AlarmBase):
    
    #def __init__(self):
    #    self.client = boto3.client('cloudwatch', 'ap-south-1')
    #    self.redis_client = boto3.client('elasticache', 'ap-south-1')
    #    self.Actions = 'abc' 
    def _get_hardware_size(self, CacheClusterd ):
        '''
         :params: CacheClusterId
         :params: region aws region name 
         :return: redis memory size(G) and networkbandwidth(gps)
        '''  
        #client = boto3.client('elasticache', region)
        response = self.redis_client.describe_cache_clusters(
            CacheClusterId=CacheClusterd
        )
        if response:
            try:
                CacheNodeType = response['CacheClusters'][0]['CacheNodeType']
                memory_size = redis_hardware_info.get(CacheNodeType)[0]['memory']
                network_bandwidth = redis_hardware_info.get(CacheNodeType)[0]['network'] 
                self.memory_size = float(memory_size) 
                self.networkout_bandwidth = float(network_bandwidth)    
            except Exception as e:
                print('不存在此实例硬件信息') 
                sys.exit(1)
    
    def create_networkout_alarm(self, CacheClusterId, CacheNodeId='0001'):
        self.client.put_metric_alarm(
            AlarmName = 'Redis-{}-NetworkBytesOut'.format(CacheClusterId),
            AlarmDescription = 'NetworkBytesOut exceed 90% of Max',
            ActionsEnabled = True,
            OKActions = [ self.OKActions,],
            AlarmActions = [ self.AlarmActions,],
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
    
           Period = self.Period,
           #Unit = 'Percent',
           EvaluationPeriods = 3,
           # 阈值为实例网络输出每分钟的字节数x90%
           Threshold = int(self.networkout_bandwidth*pow(1024,3)*60/8*0.9),  
           ComparisonOperator = 'GreaterThanThreshold'
           )
    
    def create_memory_alarm(self, CacheClusterd, CacheNodeId='0001'): 
        self.client.put_metric_alarm(
            AlarmName = 'Redis-{}-Low-FreeableMemory'.format(CacheClusterd),
            AlarmDescription = 'FreeableMemory less than 20%',
            ActionsEnabled = True,
            OKActions = [ self.OKActions,],
            AlarmActions = [ self.AlarmActions,],
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
           Period = self.Period,
           #Unit = 'Percent',
           EvaluationPeriods = 1,
           Threshold = int(self.memory_size*pow(1024,3)*0.2),  
           ComparisonOperator = 'LessThanThreshold'
           )
    
    def create_cpu_alarm(self,CacheClusterId,CacheNodeId='0001'): 
        self.client.put_metric_alarm(
            AlarmName = 'Redis-{}-High-cpu'.format(CacheClusterId),
            AlarmDescription = 'cpu util more than 80%',
            ActionsEnabled = True,
            OKActions = [ self.OKActions,],
            AlarmActions = [ self.AlarmActions,],
            MetricName = 'EngineCPUUtilization', 
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
            Period = self.Period,
            #Unit = 'Percent',
            EvaluationPeriods = 1,
            Threshold = 80,
            ComparisonOperator = 'GreaterThanThreshold'
            )
    
    def create_swap_alarm(self,CacheClusterId, CacheNodeId='0001'): 
        self.client.put_metric_alarm(
            AlarmName = 'Redis-{}-High-swap'.format(CacheClusterId),
            AlarmDescription = 'swap more than 50M',
            ActionsEnabled = True,
            OKActions = [ self.OKActions,],
            AlarmActions = [ self.AlarmActions,],
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
            Period = self.Period,
    
           #Unit = 'Percent',
           EvaluationPeriods = 1,
           Threshold = 50*pow(1024,2),   #阈值为50M
           ComparisonOperator = 'GreaterThanThreshold'
           )
    
    def create_alarm_sets(self,CacheClusterId):    
        try:
            #self.region_detect(region)
            self._get_hardware_size(CacheClusterId)
           # print self.Actions
            self.create_networkout_alarm(CacheClusterId)
            self.create_memory_alarm(CacheClusterId)
            self.create_cpu_alarm(CacheClusterId) 
            self.create_swap_alarm(CacheClusterId) 
            print "add cache:'{}' alarm success".format(CacheClusterId)
        except Exception,e:
            print(e)
r='us-west-2'
b='ap-south-1'
a = redis_alarm()
c='distribute-lock'
a.create_alarm_sets(c)
