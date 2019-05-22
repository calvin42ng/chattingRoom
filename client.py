# -*-coding:utf-8-*-

# Client
# Author: Calvin (Lin Jian-Feng)
# Email: designer@calvinlam.top
# Website: calvinlam.top

import socket
import threading

import re
patt=r'i'

outString = ''
inString = ''
nick = ''

#发送信息的函数
def DealOut(sock):
    global nick,outString #声明为全局变量，进行赋值,这样才可以生效
    while True:
        outString = input() #输入
        outString = nick + b': ' + outString.encode("utf-8") #拼接cd
        
        sock.send(outString)#发送

#接收信息
def DealIn(sock):
    global inString
    while True:
        try:
            inString = sock.recv(1024)
            if not inString:
                break
            if outString != inString:
                print(inString.decode('utf-8'))
        except:
            break



nick = input('input your nickname:')#名字
ip = input('input your server ip address:')#ip地址


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#创建套接字,默认为ipv4
sock.connect((ip,1111)) #发起请求，接收的是一个元组
nick = nick.encode("utf-8")
sock.send(nick)

#多线程  接收信息 发送信息
thin = threading.Thread(target=DealIn,args=(sock,))#调用threading 创建一个接收信息的线程'
thin.start()

thout = threading.Thread(target=DealOut,args=(sock,))#    创建一个发送信息的线程，声明是一个元组
thout.start()