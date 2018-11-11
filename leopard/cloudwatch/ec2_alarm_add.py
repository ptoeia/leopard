#!/usr/bin/env python
#coding: utf-8
#Date: 2017-11-13
#create aws ec2 cpu memory and disk alarm on aws cloudwatch

import sys
import boto3

US_WEST_2_TOPIC = 'arn:aws:sns:us-west-2:660338696248:CloudWatchAlarm'
AP_SOUTH_1_TOPIC ='arn:aws:sns:ap-south-1:660338696248:WebAlarm'

alarm_sns_arn_dict = {
                      'us-west-2': US_WEST_2_TOPIC,
                      'ap-south-1': AP_SOUTH_1_TOPIC
                     }

class ec2_alarm(object):
    """
    利用aws sdk 同时添加ec2的实例状态、cpu、
    内存和磁盘多个cloudwatch监控指标
    """
    def __init__(self,
                 instance_id,
                 PERIOD_IN_SECONDS=300,
                 Actions_SNS_TOPIC=US_WEST_2_TOPIC,
                 region='us-west-2'
                ):
        self.Actions = Actions_SNS_TOPIC 
        self.Period = PERIOD_IN_SECONDS
        self.instance_id = instance_id
        self.region = region 
        self.client = boto3.client('cloudwatch')

    def _region_detect(self, region):
        if region != 'us-west-2':
            self.Actions = alarm_sns_arn_dict.get(region)
            self.client = boto3.client('cloudwatch',region)
            
    def _get_instance_name(self):
        ec2 = boto3.resource('ec2',self.region)
        instance = ec2.Instance(self.instance_id)
        instance_name = [ tag.get('Value') 
                         for tag in instance.tags
                         if tag.get('Key')=='Name'
                        ][0]
        if not instance_name:
            print "No Name set,please set instance name first"
            sys.exit(1)
        return instance_name

    def instance_check_alarm(self, instance_name):
        self.client.put_metric_alarm(
            Statistic = 'Maximum',
            Period = self.Period,
            ActionsEnabled = True,
            #OKActions = [ self.Actions ],
            AlarmActions = [ self.Actions ],
            EvaluationPeriods = 1,
            ComparisonOperator = 'GreaterThanOrEqualToThreshold',
            AlarmName = 'EC2-{}-StatusCheckFailed'.format(instance_name),
            AlarmDescription = 'StatusCheckFailed',
            MetricName = 'StatusCheckFailed',
            Namespace = 'AWS/EC2', 
            Dimensions = [
                {
                    'Name': "InstanceId",
                    'Value': self.instance_id,
                },
            ],
            Threshold = 1,
        )

    def cpu_alarm(self, instance_name):
        self.client.put_metric_alarm(
            Statistic = 'Average',
            Period = self.Period,
            Unit = 'Percent',
            ActionsEnabled = True,
            #OKActions = [ self.Actions ],
            AlarmActions = [ self.Actions ],
            EvaluationPeriods = 1,
            ComparisonOperator = 'GreaterThanThreshold',
            AlarmName = 'EC2-{}-CPU_Utilization'.format(instance_name),
            AlarmDescription = 'CPU utilization exceed 75%',
            MetricName = 'CPUUtilization',
            Namespace = 'AWS/EC2', 
            Dimensions = [
                {
                    'Name': "InstanceId",
                    'Value': self.instance_id,
                },
            ],
            Threshold = 75,
        )

    def mem_alarm(self, instance_name):
        self.client.put_metric_alarm(
            AlarmName = 'EC2-{}-Memory_Utilization'.format(instance_name),
            AlarmDescription = 'Memory utilization exceed 90%',
            MetricName = 'MemoryUtilization',
            Namespace = 'System/Linux',
            Statistic = 'Average',
            Dimensions = [
                {
                    'Name': "InstanceId",
                    'Value': self.instance_id,
                },
            ],
            Period = self.Period,
            Unit = 'Percent',
            ActionsEnabled = True,
            #OKActions = [ self.Actions ],
            AlarmActions = [ self.Actions ],
            EvaluationPeriods = 1,
            Threshold = 90.0,
            ComparisonOperator = 'GreaterThanThreshold'
        )
    
    def disk_alarm(self, instance_name):
        self.client.put_metric_alarm(
            AlarmName = 'EC2-{}-Disk_Utilization'.format(instance_name),
            AlarmDescription = 'Disk utilization exceed 85%',
            ActionsEnabled = True,
            #OKActions = [ self.Actions, ],
            AlarmActions = [ self.Actions, ],
            MetricName = 'DiskSpaceUtilization',
            Namespace = 'System/Linux',
            Statistic = 'Average',
            Dimensions = [
                {
                    "Name":"InstanceId",
                    "Value":self.instance_id
                }, 
	        {
                    "Name":"Filesystem",
                    "Value":"/dev/xvda1"
                }, 
	       #{  实例类型为c5.xlarge时使用
               #      "Name":"Filesystem",
               #      "Value":"/dev/nvme0n1p1"
               # }, 
                {
                    "Name":"MountPath", 
                    "Value":"/"
                }
            ],
            Period = self.Period,
            Unit = 'Percent',
            EvaluationPeriods = 1,
            Threshold = 85,
            ComparisonOperator = 'GreaterThanThreshold',
        )

    def create_alarms(self):
	instance_name = self._get_instance_name()
	try:
            self._region_detect(self.region)     
            self.cpu_alarm(instance_name)
	    self.mem_alarm(instance_name)
	    self.disk_alarm(instance_name)
	    self.instance_check_alarm(instance_name)
            print "Add ec2 {} alarm metrics sucessed!".format(instance_name)
        except Exception,e:
            print(e)
            print("add cloudwatch alarm failed!")
