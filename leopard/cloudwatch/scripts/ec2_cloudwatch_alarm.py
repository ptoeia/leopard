#!/usr/bin/env python
#coding: utf-8
#Author:gewuzhang
#Date: 2017-11-13
#Create ec2 cpu memory disk alarm

import boto3
import sys
#boto3.setup_default_session(
#      aws_access_key_id = 'AKIAIGMUMPYCG2MFTZDA',
#      aws_secret_access_key = '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',
#      region_name = 'us-west-2'
#       )

def get_instance_name(instance_id):
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)
    instance_name = ''
    for each in instance.tags:
        if each['Key'] == 'Name':
            instance_name = each['Value']
            break
    if not instance_name:
        print "No Name set,please set instance_name first"
        sys.exit(1)
    else:
        return instance_name

#print get_instance_name('i-0a237133c721bca70')

def create_alarm(instance_id):
    ACTION_SNS_TOPIC = 'arn:aws:sns:us-west-2:660338696248:CloudWatchAlarm'
    PERIOD_IN_SECONDS = 300 
    instance_name = get_instance_name(instance_id)
    #if not instance_name:
    #   sys.exit(1)
    # create cpu alarm
    client = boto3.client('cloudwatch')
    client.put_metric_alarm(
        AlarmName = 'EC2-{}-CPU_Utilization'.format(instance_name),
        AlarmDescription = 'CPU utilization exceed 75%',
        ActionsEnabled = True,
        OKActions = [
            ACTION_SNS_TOPIC,
          ],
        AlarmActions = [
           ACTION_SNS_TOPIC,
         ],

        MetricName = 'CPUUtilization',
        Namespace = 'AWS/EC2',
        Statistic = 'Average',
        Dimensions = [
            {
              'Name': "InstanceId",
              'Value': instance_id,
           },
        ],
       Period = PERIOD_IN_SECONDS,
       Unit = 'Percent',
       EvaluationPeriods = 1,
       Threshold = 75,
       ComparisonOperator = 'GreaterThanThreshold',
       )
      
    #create memory alarm
    client.put_metric_alarm(
        AlarmName = 'EC2-{}-Memory_Utilization'.format(instance_name),
        AlarmDescription = 'Memory utilization exceed 90%',
        ActionsEnabled = True,
        OKActions = [
          ACTION_SNS_TOPIC,
          ],
        AlarmActions = [
          ACTION_SNS_TOPIC,
         ],
        MetricName = 'MemoryUtilization',
        Namespace = 'System/Linux"',
        Statistic = 'Average',
        Dimensions = [
         {
            'Name': "InstanceId",
            'Value': instance_id,
         },
        ],
       Period = PERIOD_IN_SECONDS,
       Unit = 'Percent',
       EvaluationPeriods = 1,
       Threshold = 90,
       ComparisonOperator = 'GreaterThanThreshold',
       )
    
     #create Root DiskPartition alarm
    client.put_metric_alarm(
        AlarmName = 'EC2-{}-Disk_Utilization'.format(instance_name),
        AlarmDescription = 'Disk utilization exceed 90%',
        ActionsEnabled = True,
        OKActions = [
          ACTION_SNS_TOPIC,
          ],
        AlarmActions = [
          ACTION_SNS_TOPIC,
         ],
        MetricName = 'DiskSpaceUtilization',
        Namespace = 'System/Linux',
        Statistic = 'Average',
        Dimensions = [
            {"Name":"InstanceId", "Value":instance_id}, 
	    {"Name":"Filesystem", "Value":"/dev/xvda1"}, 
            {"Name":"MountPath", "Value":"/"}
          ],
       Period = PERIOD_IN_SECONDS,
       Unit = 'Percent',
       EvaluationPeriods = 1,
       Threshold = 85,
       ComparisonOperator = 'GreaterThanThreshold',
       )

try:
    create_alarm('i-01cc9ea0d6595d799')
    print "Add alarm sucessed!"
except Exception,e:
    print e
    print "add cloudwatch alarm failed!"

