#!/usr/bin/env python
#-*- coding:utf-8 -*-

import boto3

#create appelb  alarm
PERIOD_IN_SECONDS = 300 

def elb_alarm(elb_arn,region='us-west-2'):
    client = boto3.client('cloudwatch')
    ACTION_SNS_TOPIC = 'arn:aws:sns:us-west-2:660338696248:CloudWatchAlarm'
    if region == 'ap-south-1':
        client = boto3.client('cloudwatch',region)
        elb_client = boto3.client('elbv2',region)
    	ACTION_SNS_TOPIC = 'arn:aws:sns:ap-south-1:660338696248:WebAlarm'

    elb_dimensions = elb_arn.split('loadbalancer/')[1]  
    elb_name = elb_arn.split('/')[2]
    response = elb_client.describe_target_groups(
        LoadBalancerArn=elb_arn,
        )
    targetgroup = response['TargetGroups'][0]['TargetGroupArn']

    #create_HTTP5XX_alarm
    client.put_metric_alarm(
        AlarmName = 'AppELB-{}-Http5XX'.format(elb_name),
        AlarmDescription = '',
        ActionsEnabled = True,
        OKActions = [ ACTION_SNS_TOPIC,],
        AlarmActions = [ ACTION_SNS_TOPIC,],
        MetricName = "HTTPCode_Target_5XX_Count",
        Namespace = 'AWS/ApplicationELB',
        Statistic = 'Sum',
        Dimensions = [
                {
                    "Name": "LoadBalancer", 
                    "Value": elb_dimensions 
                }
        ],
       Period = PERIOD_IN_SECONDS,
       #Unit = 'Percent',
       EvaluationPeriods = 1,
       Threshold = 100.0,
       ComparisonOperator = 'GreaterThanThreshold'
       )

    #create_responsetime_alarm
    client.put_metric_alarm(
        AlarmName = 'AppELB-{}-High-ReponseTime'.format(elb_name),
        AlarmDescription = 'ResponseTime exceed 0.5s',
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
       Threshold = 0.5,
       ComparisonOperator = 'GreaterThanThreshold'
       )

    #create_unhealthytargethost_alarm: 
    client.put_metric_alarm(
        AlarmName = 'AppELB-tagetgroup-{}-UnhealthyHost'.format(elb_name),
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
                   "Value": targetgroup
               }
            ], 

       Period = PERIOD_IN_SECONDS,
       #Unit = 'Percent',
       EvaluationPeriods = 1,
       Threshold = 1,
       ComparisonOperator = 'GreaterThanThreshold'
       )
