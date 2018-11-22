#!/usr/bin/env python
#coding: utf-8
#Date: 2017-11-13

import boto3
import sys

PERIOD_IN_SECONDS = 60
SNS_TOPIC = 'arn:aws:sns:us-west-2:660338696248:CloudWatchAlam'

US_WEST_2_TOPIC = 'arn:aws:sns:us-west-2:660338696248:CloudWatchAlarm'
AP_SOUTH_1_TOPIC ='arn:aws:sns:ap-south-1:660338696248:WebAlarm'

alarm_sns_arn_dict = {
                      'us-west-2': US_WEST_2_TOPIC,
                      'ap-south-1': AP_SOUTH_1_TOPIC
                     }

class AlarmBase(object):

    ActionsEnabled = True
    OKActions =  SNS_TOPIC 
    AlarmActions =  SNS_TOPIC 
    Period = PERIOD_IN_SECONDS

    def __init__(self, region):
        self.Actions = alarm_sns_arn_dict.get(region)
        self.client = boto3.client('cloudwatch',region)
        self.redis_client = boto3.client('elasticache',region)
