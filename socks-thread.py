#! /usr/bin/env python
# coding:utf-8

__author__ = 'sdm'
import socket
import sys
import select
import SocketServer
import struct

reload(sys)
sys.setdefaultencoding('utf-8')
from optparse import OptionParser


class ThreadingTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer): pass


class Socks5Server(SocketServer.StreamRequestHandler):
    def handle_tcp(self, sock, remote):
        fdset = [sock, remote]
        while True:
            r, w, e = select.select(fdset, [], [])
            if sock in r:
                if remote.send(sock.recv(4096)) <= 0: break
            if remote in r:
                if sock.send(remote.recv(4096)) <= 0: break

    def handle(self):
        global options
        try:
            print 'socks connection from ', self.client_address
            sock = self.connection
            # 1. Version
            sock.recv(262)
            sock.send(b"\x05\x00");
            # 2. Request
            data = self.rfile.read(4)
            mode = ord(data[1])
            addrtype = ord(data[3])
            if addrtype == 1:  # IPv4
                addr = socket.inet_ntoa(self.rfile.read(4))
            elif addrtype == 3:  # Domain name
                addr = self.rfile.read(ord(sock.recv(1)[0]))
            port = struct.unpack('>H', self.rfile.read(2))
            reply = b"\x05\x00\x00\x01"
            try:
                if mode == 1:  # 1. Tcp connect
                    remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    #选择某个ip出口
                    #src=('10.3.10.30',0)
                    local_ip = options.ip
                    if not local_ip is None:
                        remote.bind((local_ip, 0))
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
                if mode == 1:  # 1. Tcp connect
                    self.handle_tcp(sock, remote)
        except socket.error:
            print 'socket error'


def main():
    server = ThreadingTCPServer(('', 1080), Socks5Server)
    server.serve_forever()


def main():
    global options
    usage = '''
一个解决复杂网络的 代理服务
获取vpm 的 本地ip
ifconfig | grep ppp -A 4
ppp0: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1444
	inet 10.3.10.55 --> 10.3.10.1 netmask 0xffffff00

python socks-gevent.py -i 10.3.10.55 -p 1080
配合浏览器插件 : switchy

    '''
    parser = OptionParser(usage=usage)

    parser.add_option("-i", "--ip", dest="ip",
                      help="要的绑定ip出口的地址, unix/linux/mac  ipconfig ,windows ipconfig 获取")
    parser.add_option("-p", "--port", dest="port", default=1080, type="int",
                      help="绑定的socks5代理的本地端口推荐使用 1080 ")

    options, arg = parser.parse_args()
    #print help(options)
    #print (options['ip'])
    print('listen port:', options.port, 'local ip:', options.ip)

    server = ThreadingTCPServer(('', options.port), Socks5Server)
    server.serve_forever()


if __name__ == '__main__':
    main()
