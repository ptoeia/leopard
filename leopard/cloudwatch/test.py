#!/usr/bin/env python
import boto3

client = boto3.client('ec2')

Period = 300 

US_WEST_2_TOPIC = 'arn:aws:sns:us-west-2:660338696248:Clo:ebAlarm'

alarm_sns_arn_dict = {
                      'us-west-2': US_WEST_2_TOPIC,
                      'ap-south-1': AP_SOUTH_1_TOPIC
                     }

class redis_alarm(AlarmBase):
def region_detect(func):
    def wrapper(*args, **kwargs):
        if region != 'us-west-2':
            client = boto3.client('cloudwatch',region)
            Actions = 'abc'
            func(*args, **kwargs)
    return wrapper()

def instance_check_alarm(instance_name):
    client.put_metric_alarm(
        Statistic = 'Maximum',
        Period = Period,
        ActionsEnabled = True,
        #OKActions = [ Actions ],
        AlarmActions = [ Actions ],
        EvaluationPeriods = 1,
        ComparisonOperator = 'GreaterThanOrEqualToThreshold',
        AlarmName = 'EC2-{}-StatusCheckFailed'.format(instance_name),
        AlarmDescription = 'StatusCheckFailed',
        MetricName = 'StatusCheckFailed',
        Namespace = 'AWS/EC2', 
        Dimensions = [
            {
                'Name': "InstanceId",
                'Value': 'i-0848ffaf7784c45b9',
            },
        ],
        Threshold = 1,
    )
instance_check_alarm('test')
