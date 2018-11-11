#!/usr/bin python
#coding:utf-8
import boto3
import sys
import datetime
from datetime import datetime
from dateutil.tz import *

def get_latest_snapshot(replication_group_id):
    client = boto3.client('cloudfront')
    response = client.describe_replication_groups(
        ReplicationGroupId = replication_group_id
     )
    redis_cluster_list = response['ReplicationGroups'][0]['MemberClusters']
    #print redis_cluster_list
    if not redis_cluster_list:
        print('no snapshot')
        sys.exit(1)
    snapshot_list = []
    for each in redis_cluster_list:
        response = client.describe_snapshots(CacheClusterId=each)
        for each in response['Snapshots']:
            if each['SnapshotStatus'] == 'available':
                snapshot_list.append(
                    {
                        'SnapshotName': each['SnapshotName'],
                        'CacheSize':    each['NodeSnapshots'] [0]['CacheSize'],
                        'CreateTime':   each['NodeSnapshots'][0]['SnapshotCreateTime']
                    }
                )
    try:            
        snapshot_list.sort(key = lambda x:x['CreateTime'])
        snapshot = snapshot_list[0]
        return snapshot
    except Exception,e:
        print(e)
        print('snapshot not exits')
        sys.exit(1)
    
def create_cache(snapshot):
    client = boto3.client('elasticache')
    response = client.create_cache_cluster(
        CacheClusterId='test-review-{}'.format(datetime.now().strftime('%m%d%H%m')),
        CacheNodeType='cache.r3.large',
        NotificationTopicArn='',
        Engine='redis',
        CacheSubnetGroupName='test-env-subnet',
        SnapshotName = snapshot['SnapshotName'],
        SnapshotRetentionLimit = 0
    )
    CacheClusterId = response['CacheCluster']['CacheClusterId']
    redis_create_waiter = client.get_waiter('cache_cluster_available')
    redis_create_waiter.wait(
        CacheClusterId = CacheClusterId,
        WaiterConfig = {
                         'Delay': 30,
                         'MaxAttempts': 30
                       }
    )
    # 更新dns
    client = boto3.client('route53')
    response = client.change_resource_record_sets(
        HostedZoneId = 'Z2JNFNBSAKYRGJ',
        ChangeBatch = {
            'Comment': 'string',
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': 'review.clubfactory.test.',
                        'Type': 'CNAME',
                        'TTL': 123,
                        'ResourceRecords': [
                            {
                                'Value': CacheClusterId 
                            },
                        ],
                    }
                },
            ]
        }
    )
    waiter = client.get_waiter('resource_record_sets_changed')
    waiter.wait(Id=response['ChangeInfo']['Id'])
    ('dns udpate')

#if __name__ == '__main__':
def restore_cache(replication_group_id):
    snapshot = get_latest_snapshot(replication_group_id)
    #snapshot = get_latest_snapshot('review')
    #print snapshot
    #restore_cache(snapshot)
    create_cache(snapshot)
