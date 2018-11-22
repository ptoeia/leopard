# -*- coding: UTF-8 -*- 
from django.forms import ModelForm
from leopard.models import *
from django import forms
from django.contrib.auth.models import User 

alarm_type_choice = [
    ('ec2','ec2'),
    ('elb','elb'),
    ('rds','rds'),
    ('redis','redis')
    ]

class alarm_form(forms.Form):
    identifier = forms.CharField(required=True,widget=forms.TextInput(attrs={"placeholder":"instacne id or rds_name"}),error_messages={'required': u'必填'},)
    alarm_type = forms.ChoiceField(choices=alarm_type_choice,label='alarm type')
    region = forms.ChoiceField(choices=[
	                                       ('ap-south-1','ap-south-1'),
						                   ('us-west-2','us-west-2')
					                   ],
						               label='region')
   
class test_data_sync(forms.Form):
    cache_cluster_id = forms.CharField(required=True,widget=forms.TextInput(attrs={"placeholder":"cache cluster"}),error_messages={'required': u'必填'},)
   
