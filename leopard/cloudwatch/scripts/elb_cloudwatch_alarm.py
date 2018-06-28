#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author:gewuzhang

import boto3

#create appelb  alarm
        
def create_requestcount_alarm(elb_name,taget_name): 
    ACTION_SNS_TOPIC = 'arn:aws:sns:us-west-2:660338696248:CloudWatchAlarm'
    PERIOD_IN_SECONDS = 300 
    client = boto3.client('cloudwatch')
    client.put_metric_alarm(
        AlarmName = 'AppELB-{}-lb-Low-Requests'.format(elb_name.split('/')[1]),
        AlarmDescription = '',
        ActionsEnabled = True,
        OKActions = [ ACTION_SNS_TOPIC,],
        AlarmActions = [ ACTION_SNS_TOPIC,],
        MetricName = "RequestCount",
        Namespace = 'AWS/ApplicationELB',
        Statistic = 'Average',
        Dimensions = [
                {
                    "Name": "LoadBalancer", 
                    "Value": elb_name 
                }
            ],

       Period = PERIOD_IN_SECONDS,
       #Unit = 'Percent',
       EvaluationPeriods = 1,
       Threshold = 50.0,
       ComparisonOperator = 'LessThanThreshold'
       )

def create_responsetime_alarm(elb_name): 
    ACTION_SNS_TOPIC = 'arn:aws:sns:us-west-2:660338696248:CloudWatchAlarm'
    PERIOD_IN_SECONDS = 60 
    client = boto3.client('cloudwatch')
    client.put_metric_alarm(
        AlarmName = 'AppELB-{}-High-ReponseTime'.format(elb_name.split('/')[1]),
        AlarmDescription = 'ResponseTime exceed 3s',
        ActionsEnabled = True,
        OKActions = [ ACTION_SNS_TOPIC,],
        AlarmActions = [ ACTION_SNS_TOPIC,],
        MetricName = 'TargetResponseTime',
        Namespace = 'AWS/ApplicationELB',
        Statistic = 'Average',
        Dimensions = [
                {
                    "Name": "LoadBalancer", 
                    "Value": elb_name 
                }
            ], 

       Period = PERIOD_IN_SECONDS,
       EvaluationPeriods = 3,
       Threshold = 3.0,
       ComparisonOperator = 'GreaterThanThreshold'
       )

def create_unhealthytargethost_alarm(elb_name): 
    ACTION_SNS_TOPIC = 'arn:aws:sns:us-west-2:660338696248:CloudWatchAlarm'
    PERIOD_IN_SECONDS = 300 
    client = boto3.client('cloudwatch')
    client.put_metric_alarm(
        AlarmName = 'AppELB-tagetgroup-{}-UnhealthyHost'.format(elb_name.split('/')[1]),
        AlarmDescription = 'UnhealthyHost exceed 1',
        ActionsEnabled = True,
        OKActions = [ ACTION_SNS_TOPIC,],
        AlarmActions = [ ACTION_SNS_TOPIC,],
        MetricName = "UnHealthyHostCount",
        Namespace = 'AWS/ApplicationELB',
        Statistic = 'Average',
        Dimensions = [
                {
                    "Name": "LoadBalancer", 
                    "Value": elb_name 
                },
                {
                   "Name": "TargetGroup", 
                   "Value": targetgroup_name
               }
            ], 

       Period = PERIOD_IN_SECONDS,
       #Unit = 'Percent',
       EvaluationPeriods = 1,
       Threshold = 50.0,
       ComparisonOperator = 'LessThanThreshold'
       )

if __name__=='__main__':
    elb_name_list = ['app/pcsite-lb/dc99d9839386a9ee']
    for each in elb_name_list:    
        try:
            create_requestcount_alarm(each)
            create_responsetime_alarm(each)
            print "add elb alarm {} success".format(each)
        except Exception,e:
            print e
