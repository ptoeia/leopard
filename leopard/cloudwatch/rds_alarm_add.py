#!/usr/bin/env python
#coding: utf-8

import boto3
from alarminit import AlarmBase 

# aws rds实例的内存大小GB
rds_hardware_info = { 
    'db.m4.xlarge':{
         'memory': 16 
    },
    'db.m4.large':{
    	 'memory': 8 
    },
    'db.m4.4xlarge':{
    	 'memory': 64 
    },
    'db.m5.large':{
         'memory': 8
    },
    'db.m5.xlarge':{
         'memory': 16
    },
    'db.m3.large':{
	 'memory': 7.5
    },
    'db.r3.xlarge':{
         'memory': 30.5
    },
    'db.r3.large':{
         'memory': 15.25
    }
}

class rds_alarm(AlarmBase):

    def __init__(self,rds_name,region):
        '''
        :param rds_name rds name
        :param region aws region name
        '''
	super(rds_alarm, self).__init__(region)
    	self.rds_name = rds_name
    	self.rds_client = boto3.client('rds',region)

    def _get_hardware_info(self):
        '''
         :params: region aws region name 
         :return: redis memory size(G) and networkbandwidth(gps)
        '''  
        response = self.rds_client.describe_db_instances(
            DBInstanceIdentifier=self.rds_name
        )
        DBInstanceClass = response['DBInstances'][0]['DBInstanceClass']
        instance_type = rds_hardware_info.get(DBInstanceClass)
        if not instance_type:
            raise Exception('不存在此实例硬件信息,请更新硬件信息') 
        else:
            return int(instance_type['memory']) 

    def create_cpu_alarm(self):
        #create cpu alarm
        self.client.put_metric_alarm(
            AlarmName = 'RDS-{}-CPU_Utilization'.format(self.rds_name),
            AlarmDescription = 'CPU utilization exceed 80%',
            ActionsEnabled = True,
            #OKActions = [ self.Actions,],
            AlarmActions =[ self.Actions,],
            MetricName = 'CPUUtilization',
            Namespace = 'AWS/RDS',
            Statistic = 'Average',
            Dimensions = [ 
                {  'Name':'DBInstanceIdentifier',
                    'Value': self.rds_name
                }
            ],
            Period = self.Period,
            Unit = 'Percent',
            EvaluationPeriods = 1,
            Threshold = 80,
            ComparisonOperator = 'GreaterThanThreshold'
            )

    def create_memory_alarm(self): 
    #create FreeableMemory alarm
        self.client.put_metric_alarm(
            AlarmName = 'RDS-{}-FreeableMemory'.format(self.rds_name),
            AlarmDescription = 'FreeableMemory less than 2GB',
            ActionsEnabled = True,
            #OKActions = [ self.Actions, ],
            AlarmActions = [ self.Actions,],
            MetricName = 'FreeableMemory',
            Namespace = 'AWS/RDS',
            Statistic = 'Average',
            Dimensions = [ 
                {  'Name':'DBInstanceIdentifier',
                   'Value': self.rds_name
                }
            ],
            Period = self.Period,
            #Unit = 'Gigabytes',
            EvaluationPeriods = 1,
            Threshold = 2*pow(1024,3),
            ComparisonOperator = 'LessThanThreshold'
            )
    
    def create_storage_alarm(self): 
        #Create FreeStorageSpace alarm
        self.client.put_metric_alarm(
            AlarmName = 'RDS-{}-FreeStorageSpace_Utilization'.format(self.rds_name),
            AlarmDescription = 'FreeStorageSpace Less than 5G',
            ActionsEnabled = True,
            #OKActions = [ self.Actions,],
            AlarmActions = [ self.Actions,],
            MetricName = 'FreeStorageSpace',
            Dimensions = [ 
                {  'Name':'DBInstanceIdentifier',
                    'Value': self.rds_name
                }
            ],
            Namespace = 'AWS/RDS',
            Statistic = 'Average',
            Period = self.Period,
            #Unit = 'Megabytes',
            EvaluationPeriods = 1,
            Threshold = 5*pow(1024,3),
            ComparisonOperator = 'LessThanThreshold'
            )
    
    def create_writelatency_alarm(self): 
        #Create WriteLatency alarm
        self.client.put_metric_alarm(
            AlarmName = 'RDS-{}-High-WriteLatency'.format(self.rds_name),
            AlarmDescription = 'WriteLatency exceed 200ms',
            ActionsEnabled = True,
            #OKActions = [ self.Actions,],
            AlarmActions = [ self.Actions,],
            MetricName = 'WriteLatency',
            Dimensions = [ 
                {  'Name':'DBInstanceIdentifier',
                    'Value': self.rds_name
                }
            ],
            Namespace = 'AWS/RDS',
            Statistic = 'Average',
            Period = self.Period,
            #Unit = 'Megabytes',
            EvaluationPeriods = 1,
            Threshold = 0.2,
            ComparisonOperator = 'GreaterThanOrEqualToThreshold' 
            ) 
      
    def create_readlatency_alarm(self): 
        #Create ReadLatency alarm
        self.client.put_metric_alarm(
            AlarmName = 'RDS-{}-High-ReadLatency'.format(self.rds_name),
            AlarmDescription = 'ReadLatency exceed 200ms',
            ActionsEnabled = True,
            #OKActions = [ self.Actions,],
            AlarmActions = [ self.Actions, ],
            MetricName = 'ReadLatency',
            Dimensions = [ 
                {  'Name':'DBInstanceIdentifier',
                    'Value': self.rds_name
                }
            ],
            Namespace = 'AWS/RDS',
            Statistic = 'Average',
            Period = self.Period,
            Unit = 'Seconds',
            EvaluationPeriods = 1,
            Threshold = 0.2,
            ComparisonOperator = 'GreaterThanOrEqualToThreshold' 
            )
			
    def create_DBConnection_alarm(self,memory_size): 
        self.client.put_metric_alarm(
            AlarmName = 'RDS-{}-High-Connection'.format(self.rds_name),
            AlarmDescription = 'DBConnection more than 90% max',
            ActionsEnabled = True,
            #OKActions = [ self.Actions,],
            AlarmActions = [ self.Actions, ],
            MetricName = 'DatabaseConnections',
            Dimensions = [ 
                {  'Name':'DBInstanceIdentifier',
                   'Value': self.rds_name
                }
            ],
            Namespace = 'AWS/RDS',
            Statistic = 'Average',
            Period = self.Period,
            EvaluationPeriods = 1,
            Threshold = int(memory_size*pow(1024,3)/12582880*0.9),
            ComparisonOperator = 'GreaterThanOrEqualToThreshold' 
        )
    
    def create_alarm_sets(self):
        try:
            response = self.rds_client.describe_db_instances(
                DBInstanceIdentifier=self.rds_name,
            )
        except self.rds_client.exceptions.DBInstanceNotFoundFault,e:
            raise Exception("实例不存在") 
        else:
            memory_size=self._get_hardware_info()
            self.create_cpu_alarm()
            self.create_memory_alarm() 
            self.create_storage_alarm() 
            self.create_writelatency_alarm() 
            self.create_readlatency_alarm()
            self.create_DBConnection_alarm(memory_size) 
            print("创建成功") 

#test case
#b='us-west-2'
#m='ap-south-1'
#a=rds_alarm('sentry',b)
#a.create_alarm_sets()
