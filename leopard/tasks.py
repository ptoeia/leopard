#!/usr/bin/env python
from celery import task
from data_sync.sync_redis_from_prod import get_latest_snapshot,create_cache

@task 
def restore_cache(replication_group_id):
    snapshot = get_latest_snapshot(replication_group_id)
    restore_tatus = create_cache(snapshot)
    return restore_status
