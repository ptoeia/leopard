#!/usr/bin/env python
import ec2_alarm_add, elb_alarm_add,rds_alarm_add  
from cloudwatch.ec2_alarm_add import ec2_alarm
from cloudwatch.rds_alarm_add import rds_alarm as rds_alarm_create
from cloudwatch.elb_alarm_add import elb_alarm as elb_alarm_create

def create_alarm(resource,identifier,region='us-west-2'):
    if resouce = 'ec2':
        
        
