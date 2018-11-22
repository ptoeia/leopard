#!/usr/bin/env python
import ec2_alarm_add, elb_alarm_add,rds_alarm_add  
from ec2_alarm_add import ec2_alarm
from rds_alarm_add import rds_alarm 
from elb_alarm_add import elb_alarm 
from redis_alarm_add import redis_alarm 

def create_cloudwatch_alarm(resource,identifier,region):
    if resource == 'ec2':
        alarm = ec2_alarm(identifier,region)
        alarm.create_alarm_sets()
    elif resource == 'rds':
        alarm = rds_alarm(identifier,region)
        alarm.create_alarm_sets()
    elif resource == 'redis':
        alarm = redis_alarm(identifier,region)
        alarm.create_alarm_sets()
    else:
        alarm = elb_alarm(identifier,region)
        alarm.create_alarm_sets()
