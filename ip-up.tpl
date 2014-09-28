#!/bin/sh
#
# Script which handles the routing issues as necessary for pppd,
# including for PPTP tunnels. Save this script as /etc/ppp/ip-up
# and make sure it is executable.
#
# When the ppp link comes up, this script is called with the following
# parameters
ifname=$1        # the interface name used by pppd (e.g. ppp3)
ttyname=$2       # the tty device name
speed=$3         # the tty device speed
localip=$4       # the local IP address for the interface
remoteip=$5      # the remote IP address
ipparam=$6       # the current IP address before connecting to the VPN

#参数
#echo $0 $1 $2 $3 $4 $5 $6 >/tmp/ip-up.log

#关闭之前的进程
ps aux | grep python | grep  $ifname | awk '{print "kill " $2 }' | sh

#启动虚拟环境
source $BASE_PATH/pyenv/bin/activate
/usr/bin/env python $BASE_PATH/socks-gevent.py -i $ifname  &
exit 0;