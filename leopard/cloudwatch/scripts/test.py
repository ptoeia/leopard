#!/usr/bin/env python

import boto3

client = boto3.client('elbv2')

class A(object):
  name='age'
 
class B(A):
    def x(self):
	    print A.name
	
c=B()
c.x()
print c.name
