#!/usr/bin/env python
#-*- coding:utf-8 -*-

import boto3
from alarminit import AlarmBase 

#create appelb  alarm

class elb_alarm(AlarmBase):
    def __init__(self, elb_arn, region):
        super(elb_alarm, self).__init__(region)
        self.elb_client = boto3.client('elbv2',region)
        self.elb_arn = elb_arn

    def create_alarm_sets(self):
        try:
            elb_dimensions = self.elb_arn.split('loadbalancer/')[1]  
        except Exception:
            raise Exception ('elb实例不存在或elb_name不正确')
        else:
            elb_name = self.elb_arn.split('/')[2]
            response = self.elb_client.describe_target_groups(
                LoadBalancerArn=self.elb_arn,
            )
            targetgroup = response['TargetGroups'][0]['TargetGroupArn'].split(':')[-1]
    
        #create_HTTP5XX_alarm
        self.client.put_metric_alarm(
            AlarmName = 'AppELB-{}-Http5XX'.format(elb_name),
            AlarmDescription = '',
            ActionsEnabled = True,
            OKActions = [ self.Actions,],
            AlarmActions = [ self.Actions,],
            MetricName = "HTTPCode_Target_5XX_Count",
            Namespace = 'AWS/ApplicationELB',
            Statistic = 'Sum',
            Dimensions = [
                {
                    "Name": "LoadBalancer", 
                    "Value": elb_dimensions 
                }
            ],
           Period = self.Period,
           #Unit = 'Percent',
           EvaluationPeriods = 1,
           Threshold = 150.0,
           ComparisonOperator = 'GreaterThanThreshold'
        )
    
        #create_responsetime_alarm
        self.client.put_metric_alarm(
            AlarmName = 'AppELB-{}-High-ReponseTime'.format(elb_name),
            AlarmDescription = 'ResponseTime exceed 0.2s',
            ActionsEnabled = True,
            OKActions = [ self.Actions,],
            AlarmActions = [ self.Actions,],
            MetricName = 'TargetResponseTime',
            Namespace = 'AWS/ApplicationELB',
            Statistic = 'Average',
            Dimensions = [
                {
                    "Name": "LoadBalancer", 
                    "Value": elb_dimensions 
                }
            ], 
           Period = self.Period,
           EvaluationPeriods = 3,
           Threshold = 0.2,
           ComparisonOperator = 'GreaterThanThreshold'
        )
    
        #create_unhealthytargethost_alarm: 
        self.client.put_metric_alarm(
            AlarmName = 'AppELB-tagetgroup-{}-UnhealthyHost'.format(elb_name),
            AlarmDescription = 'UnhealthyHost exceed 1',
            ActionsEnabled = True,
            OKActions = [ self.Actions,],
            AlarmActions = [ self.Actions,],
            MetricName = "UnHealthyHostCount",
            Namespace = 'AWS/ApplicationELB',
            Statistic = 'Average',
            Dimensions = [
                {
                    "Name": "LoadBalancer", 
                    "Value": elb_dimensions 
                },
                {
                   "Name": "TargetGroup", 
                   "Value": targetgroup
               }
            ], 
           Period = self.Period,
           #Unit = 'Percent',
           EvaluationPeriods = 1,
           Threshold = 1,
           ComparisonOperator = 'GreaterThanThreshold'
        )
#a='abc'
#c='us-west-2'
#b=elb_alarm(a,c)
#b.create_alarm_sets()
