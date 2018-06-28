#!/usr/bin/env python
#coding: utf-8

import boto3
'''
boto3.setup_default_session(
      aws_access_key_id = 'AKIAIGMUMPYCG2MFTZDA',
      aws_secret_access_key = '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',
      region_name = 'us-west-2'
       )
'''

'''    
   #create cpu alarm
    client = boto3.client('cloudwatch')
    client.put_metric_alarm(
        AlarmName = 'RDS {} CPU_Utilization'.format(rds_name),
        AlarmDescription = 'CPU utilization exceed 80%',
        ActionsEnabled = True,
	OKActions = [ ACTION_SNS_TOPIC,],
        AlarmActions = [
           ACTION_SNS_TOPIC,
         ],

        MetricName = 'CPUUtilization',
        Namespace = 'AWS/RDS',
        Statistic = 'Average',
        Dimensions = [ 
             {  'Name':'DBInstanceIdentifier',
                'Value': rds_name
             }
          ],
       Period = PERIOD_IN_SECONDS,
       Unit = 'Percent',
       EvaluationPeriods = 1,
       Threshold = 80,
       ComparisonOperator = 'GreaterThanThreshold'
       )
      
    #create FreeableMemory alarm
    client.put_metric_alarm(
        AlarmName = 'RDS {} FreeableMemory'.format(rds_name),
        AlarmDescription = 'FreeableMemory less than 1GB',
        ActionsEnabled = True,
        OKActions = [
          ACTION_SNS_TOPIC,
          ],
        AlarmActions = [
          ACTION_SNS_TOPIC,
         ],
        MetricName = 'FreeableMemory',
        Namespace = 'AWS/RDS',
        Statistic = 'Average',
        Dimensions = [ 
             {  'Name':'DBInstanceIdentifier',
                'Value': rds_name
             }
          ],
       Period = PERIOD_IN_SECONDS,
       #Unit = 'Gigabytes',
       EvaluationPeriods = 1,
       Threshold = 1073741824,
       ComparisonOperator = 'LessThanThreshold'
       )
    
    #Create FreeStorageSpace alarm
    client.put_metric_alarm(
        AlarmName = 'RDS {} FreeStorageSpace_Utilization'.format(rds_name),
        AlarmDescription = 'FreeStorageSpace Less than 2G',
        ActionsEnabled = True,
        OKActions = [
          ACTION_SNS_TOPIC,
          ],
        AlarmActions = [
          ACTION_SNS_TOPIC,
         ],
        MetricName = 'FreeStorageSpace',
        Dimensions = [ 
             {  'Name':'DBInstanceIdentifier',
                'Value': rds_name
             }
          ],
        Namespace = 'AWS/RDS',
        Statistic = 'Average',
       Period = PERIOD_IN_SECONDS,
       #Unit = 'Megabytes',
       EvaluationPeriods = 1,
       Threshold = 2147483648,
       ComparisonOperator = 'LessThanThreshold'
       ) 
'''
def create_alarm(rds_name):
    ACTION_SNS_TOPIC = 'arn:aws:sns:us-west-2:660338696248:CloudWatchAlarm'
    PERIOD_IN_SECONDS = 300 
    client = boto3.client('cloudwatch')
    #Create WriteLatency alarm
    client.put_metric_alarm(
        AlarmName = 'RDS-{}-High-WriteLatency'.format(rds_name),
        AlarmDescription = 'WriteLatency exceed 200ms',
        ActionsEnabled = True,
        #OKActions = [ ACTION_SNS_TOPIC,],
        AlarmActions = [ ACTION_SNS_TOPIC, ],
        MetricName = 'WriteLatency',
        Dimensions = [ 
             {  'Name':'DBInstanceIdentifier',
                'Value': rds_name
             }
          ],
        Namespace = 'AWS/RDS',
        Statistic = 'Average',
       Period = PERIOD_IN_SECONDS,
       #Unit = 'Megabytes',
       EvaluationPeriods = 1,
       Threshold = 0.2,
       ComparisonOperator = 'GreaterThanOrEqualToThreshold' 
       ) 
  
    #Create ReadLatency alarm
    client.put_metric_alarm(
        AlarmName = 'RDS-{}-High-ReadLatency'.format(rds_name),
        AlarmDescription = 'ReadLatency exceed 200ms',
        ActionsEnabled = True,
        #OKActions = [ ACTION_SNS_TOPIC,],
        AlarmActions = [ ACTION_SNS_TOPIC, ],
        MetricName = 'ReadLatency',
        Dimensions = [ 
             {  'Name':'DBInstanceIdentifier',
                'Value': rds_name
             }
          ],
        Namespace = 'AWS/RDS',
        Statistic = 'Average',
       Period = PERIOD_IN_SECONDS,
       Unit = 'Seconds',
       EvaluationPeriods = 1,
       Threshold = 0.2,
       ComparisonOperator = 'GreaterThanOrEqualToThreshold' 
       ) 
#create_alarm('account-prod')  
db_list = ['webrdsprod','message-prod','order','vendor-tracking','image-map']
for each in db_list:
    try:
        create_alarm(each)
        print "add db {} alarm success!".format(each)
    except Exception,e:
        print "failed"
        print e
