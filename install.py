#coding:utf-8
__author__ = 'sdm'

import  os
basepath=os.path.dirname(os.path.realpath(__file__))
ip_up=basepath+'/ip-up'
text = open(basepath+'/ip-up.tpl').read()
code= text.replace('$BASE_PATH',basepath)
fp=open(ip_up,'w')
fp.write(code)
fp.close()

os.chmod(ip_up,0755)
print "ln -s %s=>/etc/ppp/ip-up" % (ip_up)
os.link(ip_up,'/etc/ppp/ip-up')
