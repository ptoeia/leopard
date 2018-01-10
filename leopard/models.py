# -*- coding: UTF-8 -*- 
from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

#多个svn对应一个host，外键应该在svn表里面
'''
       
class hosts(models.Model):
    host_name = models.CharField(max_length=30)
    host_user = models.CharField(max_length=30)
    host_pass = models.CharField(max_length=50)
    host_w_ip = models.IPAddressField()
    host_w_port = models.PositiveIntegerField(max_length=10)
    host_n_ip = models.IPAddressField()
    host_n_port = models.PositiveIntegerField(max_length=10)
    host_root_pwd = models.CharField(max_length=50)
    script_dir = models.CharField(max_length=100)
    host_description = models.TextField(blank=True)
    create_user = models.CharField(max_length=10)

    def __unicode__(self):
        return self.host_name


class svns(models.Model):
    svn_name = models.CharField(max_length=20)
    svn_user = models.CharField(max_length=30)
    svn_pass = models.CharField(max_length=30)
    svn_local = models.CharField(max_length=100)
    svn_path = models.CharField(max_length=100)
    #host  = models.ForeignKey(hosts,on_delete=models.SET_NULL())
    create_user = models.CharField(max_length=10)
    def __unicode__(self):
        return self.svn_name


class hostgroup(models.Model):
    host_groupname = models.CharField(max_length=30)
    host = models.ManyToManyField(hosts)
    create_date = models.CharField(max_length=30)
    create_user = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.host_groupname

class scripts(models.Model):
    script_name = models.CharField(max_length=30)
    script_file = models.FileField(upload_to='leopard/script/')
    script_date = models.CharField(max_length=50)
    script_description = models.TextField(blank=True)
    create_user = models.CharField(max_length=10)
    def __unicode__(self):
        return self.script_name

class scriptgroup(models.Model):
    script_groupname = models.CharField(max_length=30)
    script = models.ManyToManyField(scripts)
    create_date = models.CharField(max_length=30)
    create_user = models.CharField(max_length=10)
    def __unicode__(self):
        return self.script_groupname

class tasks(models.Model):
    task_name = models.CharField(max_length=50)
    #script_group = models.ForeignKey(scriptgroup)
    #host_group = models.ForeignKey(hostgroup)
    task_date = models.CharField(max_length=50)
    task_status = models.CharField(max_length=10)
    task_create_user = models.CharField(max_length=30)
    def __unicode__(self):
        return self.task_name

class services(models.Model):
    host  = models.ForeignKey(hosts)
    service_name = models.CharField(max_length=50)
    service_script = models.CharField(max_length=100)
    service_log = models.CharField(max_length=100)

    def __unicode__(self):
        return self.service_name

class releases(models.Model):
    create_user =  models.CharField(max_length=10)
    add_time = models.CharField(max_length=30)
    add_reason = models.TextField()
    start_test_time = models.CharField(max_length=30,blank=True)
    end_test_time = models.CharField(max_length=30,blank=True)
    test_status = models.CharField(max_length=1,default='3')
    upload_file = models.FileField(upload_to='leopard/packages/',max_length=100)
    ststus_reason = models.CharField(max_length=15,blank=True)

    def __unicode__(self):
        return self.id

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(u"姓名",max_length=30)
    iphone = models.CharField(u'手机',max_length=11)
'''