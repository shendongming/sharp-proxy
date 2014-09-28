#! /usr/bin/env python
# coding:utf-8

__author__ = 'sdm'

import socket
import sys
import struct
import os
reload(sys)
sys.setdefaultencoding('utf-8')
from optparse import OptionParser

import re
import gevent
from gevent import monkey;

monkey.patch_all()

from gevent.server import StreamServer


def hanlder(sock, address):
    '''
    socks5 代理的
    '''
    global options
    print options
    rfile = sock.makefile()
    try:
        print 'socks connection from ', address
        # 1. Version
        recv_data = sock.recv(262)
        sock.sendall(b"\x05\x00");
        # 2. Request
        data = rfile.read(4)
        mode = ord(data[1])
        addrtype = ord(data[3])
        if addrtype == 1:  # IPv4
            addr = socket.inet_ntoa(rfile.read(4))
        elif addrtype == 3:  # Domain name
            # 域名长度一个字节限制
            addr = rfile.read(ord(sock.recv(1)[0]))
        port = struct.unpack('>H', rfile.read(2))
        print 'addr type:', addrtype, 'mode:', mode, 'addr:', addr, 'port:', port
        reply = b"\x05\x00\x00\x01"
        try:
            if mode == 1:  # 1. Tcp connect
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # 选择某个ip出口
                # src=('10.3.10.30',0)
                # 比如是一个 vpn的本地的ip地址
                bind_ip = options.ip
                if not bind_ip is None:
                    remote.bind((bind_ip, 0))
                print 'remote connect:', addr, port[0]
                remote.connect((addr, port[0]))

                print 'Tcp connect to', addr, port[0]
            else:
                reply = b"\x05\x07\x00\x01"  # Command not supported
            local = remote.getsockname()
            reply += socket.inet_aton(local[0]) + struct.pack(">H", local[1])
        except socket.error:
            # Connection refused
            reply = '\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00'
        sock.send(reply)
        # 3. Transfering
        if reply[1] == '\x00':  # Success
            print 'Transfering Success'
            if mode == 1:  # 1. Tcp connect
                print 'tcp connect'
                handle_tcp(sock, remote)

    except socket.error:
        print 'socket error'


def handle_tcp(sock, remote):
    fdset = [sock, remote]
    while True:
        r, w, e = gevent.select.select(fdset, [], [])
        if sock in r:
            if remote.send(sock.recv(4096)) <= 0: break
        if remote in r:
            if sock.send(remote.recv(4096)) <= 0: break

def get_ppp0():
    import netifaces as ni


def main():
    global options
    usage = '''
一个解决复杂网络的 代理服务
获取vpm 的 本地ip
ifconfig | grep ppp -A 4
ppp0: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1444
	inet 10.3.10.55 --> 10.3.10.1 netmask 0xffffff00

python socks-gevent.py -i ppp0 -p 1080  #绑定vpn 或者adsl的地址
python socks-gevent.py -i ppp1 -p 1080

使用指定ip的方式
python socks-gevent.py -i 10.3.10.55 -p 1080
配合浏览器插件 : switchy

配置好脚本
python install.py
ip-up
软连接 到
sudo ln -s %s/ip-up /etc/ppp/ip-up

    ''' % (os.path.dirname(os.path.realpath(__file__)),)
    parser = OptionParser(usage=usage)

    parser.add_option("-i", "--ip", dest="ip",
                      help="要的绑定ip出口的地址, ppp0 \n unix/linux/mac  ipconfig ,windows ipconfig 获取")
    parser.add_option("-p", "--port", dest="port", default=1080, type="int",
                      help="绑定的socks5代理的本地端口推荐使用 1080 ")

    options, arg = parser.parse_args()
    print "opt:",options

    if not options.ip is None and  options.ip[0:3]=='ppp':
        '使用指定接口的方式'
        import netifaces as ni
        interfaces=ni.interfaces()
        if not options.ip in interfaces:
            print("error  interface error,available interface:\n")
            for p  in interfaces:
                print p
            return
        a=ni.ifaddresses(options.ip)
        print 'a',a
        print a
        if not a.has_key(2) or not len(a[2]) :
            print "接口错误"
            return
        options.ip=a[2][0]['addr']
        print("new ip",options.ip)

    print('listen port:', options.port, 'local ip:', options.ip)
    server = gevent.server.StreamServer(('', options.port), hanlder)
    server.serve_forever()


if __name__ == '__main__':
    main()
