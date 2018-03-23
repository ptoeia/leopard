from django.conf.urls import  include, url
from leopard.views import * 
from django.contrib import admin
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'leopardproject.views.home', name='home'),
    # url(r'^leopardproject/', include('leopardproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^loginout/$', 'loginout',name='logout'),

    url(r'^$', index),
    url(r'^alarm_add',alarm_add),

]
