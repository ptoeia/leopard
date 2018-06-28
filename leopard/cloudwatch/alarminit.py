#!/usr/bin/env python
#coding: utf-8
#Author:gewuzhang
#Date: 2017-11-13
#Create ec2 cpu memory disk alarm

import boto3
import sys

class AlarmBase(object):
    def __init__(self,
                 PERIOD_IN_SECONDS = 60,
                 SNS_TOPIC = 'arn:aws:sns:us-west-2:660338696248:CloudWatchAlam'
                 ): 
        self.ActionsEnabled = True,
        self.OKActions = [ SNS_TOPIC ]
        self.AlarmActions = [ SNS_TOPIC ]
        self.Period = PERIOD_IN_SECONDS
        
       
    def put_alarm(self,**kwagrgs):
        client = boto3.client('cloudwatch')
        client.put_metric_alarm(
               Statistic = 'Average',
               Period = self.Period, 
               Unit = 'Percent',
               ActionsEnabled = self.ActionsEnabled, 
               OKActions = [ ACTION_SNS_TOPIC ],
               AlarmActions = [ ACTION_SNS_TOPIC ],
               EvaluationPeriods = 1,
               ComparisonOperator = 'GreaterThanThreshold'
             )
