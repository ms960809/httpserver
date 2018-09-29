#-*- coding:utf-8 -*-
'''
name:Jiaopengbo
time: 2018-10-01
'''

from socket import *
import sys
import re
from threading import Thread
from setting import *
import time


class HTTPServer(object):
    def __init__(self,addr = ('0.0.0.0',80)):
        self.addr = addr
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.bind(addr)

    #绑定服务端地址
    def bind(self,addr):
        self.ip = addr[0]
        self.port = addr[1]
        self.sockfd.bind(addr)

    #启动服务器
    def serve_forever(self):
        self.sockfd.listen(5)
        print('Listen the port %d' % self.port)
        while 1:
            connfd,addr = self.sockfd.accept()
            print('Connect from',addr)
            # 当有客户端连接时创建新的线程
            headle_client = Thread(target = self.headle_request,args = (connfd,))
            headle_client.setDaemon(True)
            headle_client.start()

    def headle_request(self,connfd):
        #接受浏览器请求
        request = connfd.recv(4096)
        request_lines = request.splitlines()
        # 获取请求行
        request_line = request_lines[0].decode()
        #正则表达式
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)'
        try:
            env = re.match(pattern,request_line).groupdict()
        except:
            response_headlers = 'HTTP/1.1 500 Server Error\r\n'
            response_headlers += '\r\n'
            response_body = 'Server Error'
            response = response_headlers + response_body 
            connfd.send(response.encode())
            return
        #将请求发给frame得到返回数据结果
        status,response_body = self.send_request(env['METHOD'],env['PATH'])
        #根据响应吗组织响应头内容
        print('======')
        response_headlers = self.get_headlers(status)
        print('=====')
        #将结果组织委员http response 发送给客户端
        response = response_headlers + response_body
        connfd.send(response.encode())
        connfd.close()

    #和frame交互　发送request获取response
    def send_request(self,method,path):
        s = socket()
        s.connect(frame_addr)
        #向webframe发送method和path
        s.send(method.encode())
        time.sleep(0.1)
        s.send(path.encode())
        status = s.recv(128).decode()
        response_body = s.recv(409600000).decode()
        return status,response_body

    def get_headlers(self,status):
        if status == '200':
            response_headlers = 'HTTP/1.1 200 OK\r\n'
            response_headlers += '\r\n'
        elif status == '404':
            response_headlers = 'HTTP/1.1 404 Not Found\r\n'
            response_headlers += '\r\n'
        return response_headlers


if __name__ == '__main__':
    httpd = HTTPServer(ADDR)
    httpd.serve_forever()