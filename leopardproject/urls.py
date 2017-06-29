from django.conf.urls import patterns, include, url
from django.contrib import admin
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('leopard.views',
    # Examples:
    # url(r'^$', 'leopardproject.views.home', name='home'),
    # url(r'^leopardproject/', include('leopardproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'login'),
    url(r'^loginout/$', 'loginout',name='logout'),
    url(r'^$', 'index'),
    url(r'^svnadd/$', 'svnadd'),
    url(r'^hostadd/$', 'hostadd'),
    url(r'^hostedit/(?P<host_id>[^/]+)$', 'hostedit',name='hostedit'),
    url(r'^hostdel/(?P<host_id>[^/]+)$', 'hostdel',name='hostdel'),
    url(r'^confirm_del/(?P<host_id>[^/]+)$', 'confirm_del'),
    url(r'^showsvn/$', 'showsvn',name='showsvn'),
    url(r'^showsvnlog/$', 'showsvnlog'),
    url(r'^svnedit/(?P<svn_id>[^/]+)$', 'svnedit',name='svnedit'),
    url(r'^svnupdate/(?P<svn_id>[^/]+)/(?P<u_type>[^/]+)$', 'svnupdate', name='svnupdate'),
    url(r'^group/$', 'group',name='group'),
    url(r'^task/$', 'task',name='task'),
    url(r'^task_del/(?P<task_id>[^/]+)$', 'task_del', name='task_del'),
    url(r'^task_status/(?P<task_id>[^/]+)$', 'task_status',name='task_status'),
    url(r'^task_run/$', 'task_run'),
    url(r'^addtogroup/$', 'addtogroup'),
    url(r'^addscript/$', 'addscript'),
    url(r'^showscript/$', 'showscript',name='showscript'),
    url(r'^delscript/(?P<script_id>[^/]+)$', 'scriptdel',name='scriptdel'),
    url(r'^hostgroup_detail/(?P<group_id>[^/]+)$', 'hostgroup_detail',name='hostgroup_detail'),
    url(r'^hostgroup_del/(?P<group_id>[^/]+)$', 'hostgroup_del',name='hostgroup_del'),
    url(r'^scriptgroup_detail/(?P<group_id>[^/]+)$', 'scriptgroup_detail', name='scriptgroup_detail'),
    url(r'^scriptgroup_del/(?P<group_id>[^/]+)$', 'scriptgroup_del', name='scriptgroup_del'),
    url(r'^hostgroup_del_host/$', 'hostgroup_del_host'),
    url(r'^scriptgroup_del_script/$', 'scriptgroup_del_script'),
    url(r'^showuser/$', 'showuser',name='showuser'),
    url(r'^adduser/$', 'adduser'),
    url(r'^edituser/(?P<user_id>[^/]+)$', 'edituser',name='useredit'),
    url(r'^deluser/(?P<user_id>[^/]+)$', 'deluser',name='userdel'),
    #url(r'^test/$', 'test'),
    url(r'^showservice/$', 'showservice',name='showservice'),
    url(r'^addservice/$', 'addservice',),
    url(r'^addrelease/$','addrelease'),
    url(r'^showrelease/$','showrelease',name='showrelease'),
    
)
