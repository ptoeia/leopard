#!/usr/bin/env python

import boto3

client = boto3.client('elbv2')

tg=client.describe_targetgroup()
