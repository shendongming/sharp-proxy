sharp-proxy
===========

一个 代理程序,解决网络复杂的问题(你懂的)

假如你的电脑有2个网络出口
你想让你的程序可以自由选择出口,那么这个正适合你
例如:adsl+vpm(n)
或者 adsl+3G 网络

----
实现方法

为每个ip出口启动一个代理服务

你的程序要从某个出口出,那么让你的app 从 某个代理出去 即可


-----
安装方法:
 首先你要安装 py2.7

    socks-thread.py 基于线程的版本 (不在维护了)
    socks-gevent.py 基于gevent的版本   pip install gevent



使用方法:
----

    python sharp-proxy/socks-gevent.py --help
    $ python socks-gevent.py --help
    Usage:
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
    sudo ln -s /Users/sdm/share/code/sharp-proxy/ip-up /etc/ppp/ip-up
    
    
    
    Options:
      -h, --help            show this help message and exit
      -i IP, --ip=IP        要的绑定ip出口的地址, ppp0   unix/linux/mac
                            ipconfig ,windows ipconfig 获取
      -p PORT, --port=PORT  绑定的socks5代理的本地端口推荐使用 1080
    #配置 ppp自动启动代理脚本 
    sudo python install.py
    ln -s /Users/sdm/share/code/sharp-proxy/ip-up=>/etc/ppp/ip-up

----

todo:socks5 代理转 http 代理
==============

python sharp-proxy/socks2http.py  -src 1080 -to 1082