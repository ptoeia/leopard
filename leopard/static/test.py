#!/usr/bin/env python
import os
import json 
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

ali_yun_access_key_Id='LTAIHBRbS8QAe9ay'
ali_yun_AccessKeySecret='xJh0vPKYhYhky66zjD4Fdz4ZSROEGM'

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
print aliyun_rds_count('erp')
print aliyun_rds_count('midware')
