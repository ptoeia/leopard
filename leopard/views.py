# -*- coding: UTF-8 -*- 
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
from leopard.form import alarm_form,test_data_sync
from django.shortcuts import render, render_to_response, Http404, get_object_or_404, RequestContext
from leopardproject import settings
from cloudwatch.ec2_alarm_add import ec2_alarm
from cloudwatch.rds_alarm_add import rds_alarm as rds_alarm_create
from cloudwatch.elb_alarm_add import elb_alarm as elb_alarm_create
from static.static import mapping
#from data_sync.sync_redis_from_prod import restore_cache
from django.contrib.auth.models import User  
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required
#from function import *
from tasks import restore_cache
#import restore_cache
import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")

def index(request):
    return render_to_response('task.html')

def alarm_add(request):
    if request.method == 'POST':
        form = alarm_form(request.POST)
        if form.is_valid():
            #selected_alarm_type = request.POST['alarm_type']
            selected_alarm_type = form.cleaned_data['alarm_type']
            identifier = form.cleaned_data['identifier']
            region = form.cleaned_data['region']
            if selected_alarm_type == 'ec2':
                alarm = ec2_alarm(identifier,region=region)
                try:
                    alarm.create_alarms()
                    return HttpResponse('ok')
                except Exception, e:
                    return HttpResponse(e) 
            if selected_alarm_type == 'rds':
                try:
                    rds_alarm_create(identifier,region)
                    return HttpResponse('ok')
                except Exception, e:
                   return HttpResponse(e)
            if selected_alarm_type == 'elb':
                try:
                    elb_alarm_create(identifier,region)
                    return HttpResponse('ok')
                except Exception, e:
                   return HttpResponse(e)
    else:      
        form = alarm_form()
    return render_to_response('alarm_add.html',{'alarm_add_form':form}) 

def data_sync(request):
    if request.method == 'POST':
        form = test_data_sync(request.POST)
        if form.is_valid():
            cache_cluster_id = request.POST['cache_cluster_id']
            try:
                restore_cache.delay(cache_cluster_id)
            except Exception, e:
                return HttpResponse(e)
    else:
        form = test_data_sync()
    return render_to_response('data_sync.html',{'form':form})

def count(request):
    if request.method == 'POST':
        map = mapping() 
    return render_to_response('static.html')    
    
def link(request):
    return render_to_response('link.html')    
