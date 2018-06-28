#!/usr/bin/env python
#coding: utf-8
#Date: 2017-11-13
#create ec2 cpu memory and disk alarm on aws cloudwatch

import boto3
import sys
from alarminit import AlarmBase

#client = boto3.client('cloudwatch',aws_access_key_id='AKIAIYP7DIYMDWZOOWAA',aws_secret_access_key='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')
client = boto3.client('cloudwatch')
class ec2_alarm(object):
    def __init__(self,
              instance_id,
              PERIOD_IN_SECONDS = 300,
              #Actions_SNS_TOPIC = 'arn:aws:sns:us-west-2:660338696248:CloudWatchAlarm'
              Actions_SNS_TOPIC = 'arn:aws:sns:us-west-2:660338696248:abc',
              ):
        self.Actions = Actions_SNS_TOPIC 
        self.Period = PERIOD_IN_SECONDS
        self.instance_id = instance_id

    def __get_instance_name(self):
        ec2 = boto3.resource('ec2')
        instance = ec2.Instance(self.instance_id)
        instance_name = ''
        for each in instance.tags:
            if each['Key'] == 'Name':
                instance_name = each['Value']
                break
        if not instance_name:
            print "No Name set,please set instance name first"
            sys.exit(1)
        else:
            return instance_name

    def _instance_check_alarm(self,**kwargs):
        instance_name = self.__get_instance_name()
        client = boto3.client('cloudwatch')
        client.put_metric_alarm(
               Statistic = 'Maximum',
               Period = self.Period,
               ActionsEnabled = True,
               OKActions = [ self.Actions ],
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
    def cpu_alarm(self,**kwargs):
        instance_name = self.__get_instance_name()
        client = boto3.client('cloudwatch')
        client.put_metric_alarm(
               Statistic = 'Average',
               Period = self.Period,
               Unit = 'Percent',
               ActionsEnabled = True,
               OKActions = [ self.Actions ],
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

    def mem_alarm(self,**kwargs):
        instance_name = self.__get_instance_name()
        client.put_metric_alarm(
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
           OKActions = [ self.Actions ],
           AlarmActions = [ self.Actions ],
           EvaluationPeriods = 1,
           Threshold = 90.0,
           ComparisonOperator = 'GreaterThanThreshold'
           )
    
    #create Root DiskPartition alarm,
    def disk_alarm(self,**kwargs):
        instance_name = self.__get_instance_name()
        client.put_metric_alarm(
            AlarmName = 'EC2-{}-Disk_Utilization'.format(instance_name),
            AlarmDescription = 'Disk utilization exceed 85%',
            ActionsEnabled = True,
            OKActions = [ self.Actions ],
            AlarmActions = [ self.Actions, ],
            MetricName = 'DiskSpaceUtilization',
            Namespace = 'System/Linux',
            Statistic = 'Average',
            Dimensions = [
                {"Name":"InstanceId", "Value":self.instance_id}, 
	            #{"Name":"Filesystem", "Value":"/dev/xvda1"}, 
	            {"Name":"Filesystem", "Value":"/dev/nvme0n1p1"}, 
                {"Name":"MountPath", "Value":"/"}
            ],
            Period = self.Period,
            Unit = 'Percent',
            EvaluationPeriods = 1,
            Threshold = 85,
            ComparisonOperator = 'GreaterThanThreshold',
          )

    def create_alarms(self):
	instance_name = self.__get_instance_name()
	print instance_name
	try:
            self.cpu_alarm()
	    self.mem_alarm()
	    self.disk_alarm()
	    self.instance_status_alarm()
            print "Add alarm sucessed!"
        except Exception,e:
            print(e)
            print("add cloudwatch alarm failed!")

#if __name__=='__main__':
#    id = sys.argv[1]
#    a=ec2_alarm(id)
#    a.create_alarms()
