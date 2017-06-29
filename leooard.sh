#!/bin/bash
case $1 in
 stop) ps aux | grep manage.py | grep -v grep | awk '{print "kill -9",$2}' | sh && rm -rf /tmp/python.sock;;
 start) python /var/www/leopard-master/manage.py runfcgi socket=/tmp/python.sock maxrequests=1 && chown nginx.nginx /tmp/python.sock;;
 *) echo "stop|start";;
esac

