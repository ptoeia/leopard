#!/usr/bin/env python

import redis
import boto3

pool = redis.ConnectionPool(host='127.0.0.1',password='')
r = redis.ConnectionPool(connection_pool=pool)

region='us-west-2'
client = boto3.client('rds',region)
response = client.describe_db_instances()
for instance in response['DBInstances']:
    print instance['DBInstanceIdentifier'],instance['DBInstanceArn']
