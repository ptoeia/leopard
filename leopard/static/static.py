#!/usr/bin/env python
#-*-coding:utf-8

import os
import json
import boto3

import matplotlib as mpl
mpl.use('Agg')

import numpy as np
import matplotlib.pyplot as plt

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

ali_yun_access_key_Id='LTAIHBRbS8QAe9ay'
ali_yun_AccessKeySecret='xJh0vPKYhYhky66zjD4Fdz4ZSROEGM'

ALIYUN_MIDWARE_REDIS_COUNT = 1
ALIYUN_ERP_REDIS_COUNT = 11
AWS_ERP_REDIS_COUNT = 1

PNG_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def aliyun_ecs_count(value, key='Group', region='cn-hangzhou'):
    """
    return count of aliyun ecs with:
      -- specific tag 
      -- in runing status
    """ 
    client = AcsClient(ali_yun_access_key_Id, ali_yun_AccessKeySecret,region)
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('ecs.aliyuncs.com')
    request.set_method('POST')
    request.set_version('2014-05-26')
    request.set_action_name('DescribeInstances')

    request.add_query_param('Tag.1.value', value)
    request.add_query_param('Tag.1.key', key)
    request.add_query_param('RegionId', region)
    request.add_query_param('Status', 'Running')

    response = client.do_action_with_exception(request)
    return  json.loads(response)['TotalCount']

def aliyun_rds_count(value, key='Group', region='cn-hangzhou'):
    client = AcsClient(ali_yun_access_key_Id, ali_yun_AccessKeySecret,region)
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('rds.aliyuncs.com')
    request.set_method('POST')
    request.set_version('2014-08-15')
    request.set_action_name('DescribeTags')
   
    request.add_query_param('RegionId', region)
    request.add_query_param('Tags', str({key:value}))
    response = client.do_action_with_exception(request)
    rds_count = len(json.loads(response)['Items']['TagInfos'][0]['DBInstanceIds']['DBInstanceIds'])
    return rds_count 


def aws_ec2_count(value,region='us-west-2'):
    client = boto3.client('ec2',region)
    response = client.describe_instances(
        Filters = [
            {
                'Name': 'tag:Group',
                'Values': [
                     value,
                ]
            },
            {
                'Name': 'instance-state-code',
                'Values': [
                     '16',
                ]
            } 
        ],
    )
    instance_id_list = [ 
        each['Instances'][0]['InstanceId'] for each in response['Reservations']
        ]
    return len(instance_id_list)

def aws_rds_count(value, region='us-west-2'):
    client = boto3.client('rds',region)
    response = client.describe_db_instances()
    #以下逻辑可以考虑使用map 
    count = 0
    for each in response['DBInstances']:
        list_response = client.list_tags_for_resource(
            ResourceName=each['DBInstanceArn']
        )
        tag_list = list_response['TagList']
        for tag in tag_list:
            if tag['Key'] == 'Group' and tag['Value'] == value:
               count+=1
    return count 

def aws_redis_count(value, region='us-west-2'):
    redis_arn_prefix='arn:aws:elasticache:{}:660338696248:cluster'.format(region)
    client = boto3.client('elasticache',region)
    response = client.describe_cache_clusters()
    count = 0
    for each in response['CacheClusters']:
        if each['CacheClusterStatus'] == 'available': 
            list_tags_response = client.list_tags_for_resource(
                ResourceName='{}:{}'.format(redis_arn_prefix,each['CacheClusterId'])
            )
            tag_list = list_tags_response['TagList']
            for tag in tag_list:
                if tag['Key'] == 'Group' and tag['Value'] == value:
                   count+=1
    return count

def mapping():
    #中文乱码解决
   # plt.rcParams['font.sans-serif'] =['Microsoft YaHei']
   # plt.rcParams['axes.unicode_minus'] = False
   # plt.rc('font', family='SimHei', size=13)
    plt.style.use('ggplot') 
    
    erp_ec2_count = int(aliyun_ecs_count('erp')) + int(aws_ec2_count('erp',region='ap-south-1'))
    erp_rds_count = int(aliyun_rds_count('erp')) + int(aws_rds_count('erp',region='ap-south-1'))
    erp_redis_count = aws_redis_count('erp') + aws_redis_count('erp',region='ap-south-1') + ALIYUN_ERP_REDIS_COUNT 
    
    midware_ec2_count = int(aliyun_ecs_count('midware'))+int(aws_ec2_count('midware'))
    midware_rds_count = int(aliyun_rds_count('midware'))+int(aws_rds_count('midware'))
    midware_redis_count = int(ALIYUN_MIDWARE_REDIS_COUNT)+int(aws_rds_count('midware'))

    app_resource_count = [aws_ec2_count('app')+aliyun_ecs_count('app'),aws_rds_count('app'),aws_redis_count('app')] 
    midware_resource_count = [midware_ec2_count,midware_rds_count,midware_redis_count] 
    erp_resource_count = [erp_ec2_count,erp_rds_count,erp_redis_count] 
    
    index=np.arange(3)
    bar_width=0.3
    plt.subplot(221)  
    plt.bar(index, app_resource_count, width=0.3, label='app',color='steelblue')
    plt.bar(index + bar_width, erp_resource_count, width=0.3, label='erp',color='green')
    plt.bar(index + bar_width*2, midware_resource_count, width=0.3, label='midware',color='y')
    
    plt.legend()

    #plt.xlabel(u'类别')
    plt.ylabel(u'count')
    plt.title(u'cloud resource')
   
    plt.xticks(range(3),['ec2','rds','redis'],fontsize='12')
    for x,y in enumerate(app_resource_count):
        plt.text(x,y,'%s' %y,va='center',ha='center',fontsize='10',color = "r")

    for x,y in enumerate(erp_resource_count):
        plt.text(x+bar_width,y,'%s' %y,va='center',ha='center',fontsize='10',color = "r")
    
    for x,y in enumerate(midware_resource_count):
        plt.text(x+bar_width*2,y,'%s' %y,va='center',ha='center',fontsize='10',color = "r")
  
    # 阿里云资源统计
    plt.subplot(223)
        
    erp_ec2_count_aliyun =  \
                aliyun_ecs_count('erp') + \
                aliyun_ecs_count('erp',region='cn-shenzhen')
    erp_rds_count_aliyun =  \
                aliyun_rds_count('erp') + \
                aliyun_rds_count('erp',region='cn-shenzhen')
    erp_redis_count_aliyun  = 11

    midware_ec2_count_aliyun = aliyun_ecs_count('midware')
    midware_rds_count_aliyun = aliyun_rds_count('midware')
    midware_redis_count_aliyun = ALIYUN_MIDWARE_REDIS_COUNT

    app_ec2_count_aliyun = aliyun_ecs_count('app') 
    app_rds_count_aliyun = aliyun_rds_count('app')
    app_redis_count_aliyun  = 1

    app_aliyun_resource_count = [ aliyun_ecs_count('app'), aliyun_ecs_count('app'),app_redis_count_aliyun] 
    midware_aliyun_resource_count = [midware_ec2_count_aliyun,midware_rds_count_aliyun,midware_redis_count] 
    erp_aliyun_resource_count = [erp_ec2_count_aliyun,erp_rds_count_aliyun,erp_redis_count_aliyun] 
    #print app_aliyun_resource_count, midware_aliyun_resource_count, erp_aliyun_resource_count 
    plt.bar(index, app_aliyun_resource_count, width=0.3, label='app',color='steelblue')
    plt.bar(index + bar_width, erp_aliyun_resource_count, width=0.3, label='erp',color='green')
    plt.bar(index + bar_width*2, midware_aliyun_resource_count, width=0.3, label='midware',color='y')
    
    plt.legend()

    plt.ylabel(u'count')
    #plt.title(u'aliyun resource',loc ='left')
   
    plt.xticks(range(3),['ec2','rds','redis'],fontsize='12')
    for x,y in enumerate(app_aliyun_resource_count):
        plt.text(x,y,'%s' %y,va='center',ha='center',fontsize='10',color = "r")

    for x,y in enumerate(erp_aliyun_resource_count):
        plt.text(x+bar_width,y,'%s' %y,va='center',ha='center',fontsize='10',color = "r")
    
    for x,y in enumerate(midware_aliyun_resource_count):
        plt.text(x+bar_width*2,y,'%s' %y,va='center',ha='center',fontsize='10',color = "r")
  
  
    # aws资源统计
    plt.subplot(224)
        
    erp_ec2_count_aws =  \
                aws_ec2_count('erp',region='ap-south-1')
    erp_rds_count_aws =  \
                aws_rds_count('erp',region='ap-south-1')
    erp_redis_count_aws  = aws_redis_count('erp',region='ap-south-1')

    midware_ec2_count_aws = aws_ec2_count('midware')
    midware_rds_count_aws = aws_rds_count('midware')
    midware_redis_count_aws = aws_redis_count('midware')

    app_ec2_count_aws = aws_ec2_count('app') 
    app_rds_count_aws = aws_rds_count('app')
    app_redis_count_aws  = aws_redis_count('app')

    app_aws_resource_count = [ aws_ec2_count('app'),aws_rds_count('app'),aws_redis_count('app')] 
    midware_aws_resource_count = [ aws_ec2_count('midware'),aws_rds_count('midware'),aws_redis_count('midware')] 
    erp_aws_resource_count = [
                                 aws_ec2_count('erp',region='ap-south-1'),
                                 aws_rds_count('erp',region='ap-south-1'),
                                 aws_redis_count('erp',region='ap-south-1')
                              ] 
    plt.bar(index, app_aws_resource_count, width=0.3, label='app',color='steelblue')
    plt.bar(index + bar_width, erp_aws_resource_count, width=0.3, label='erp',color='green')
    plt.bar(index + bar_width*2, midware_aws_resource_count, width=0.3, label='midware',color='y')
    
    plt.legend()

    plt.ylabel(u'count')
    plt.title(u'aws resource',loc ='left')
   
    plt.xticks(range(3),['ec2','rds','redis'],fontsize='12')
    for x,y in enumerate(app_aws_resource_count):
        plt.text(x,y,'%s' %y,va='center',ha='center',fontsize='12',color = "r")

    for x,y in enumerate(erp_aws_resource_count):
        plt.text(x+bar_width,y,'%s' %y,va='center',ha='center',fontsize='10',color = "r")
    
    for x,y in enumerate(midware_aws_resource_count):
        plt.text(x+bar_width*2,y,'%s' %y,va='center',ha='center',fontsize='10',color = "r")

    plt.savefig('{}/static/img/ec_count.png'.format(PNG_DIR))
    plt.close()
