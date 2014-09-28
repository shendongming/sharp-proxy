#coding:utf-8
__author__ = 'sdm'

import socks
import socket
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 8080)
socket.socket = socks.socksocket
import urllib2
print urllib2.urlopen('http://www.google.com').read()

a=urllib2.urlopen('http://localhost/info.php');
print a.read()