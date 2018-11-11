#!/usr/bin/env python
import boto3
client = boto3.client('ec2')
response = client.describe_tags(
    Filters=[
        {
            'Name': 'resource-type',
            'Values': [
                'instance',
            ]
        },
        {
            'Name': 'tag:Name',
            'Values': [
                'app-*',
            ]
        },
    ],
)
print (response['Tags'])
