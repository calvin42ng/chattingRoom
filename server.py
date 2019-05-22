# -*-coding:utf-8-*-

# Server
# Author: Calvin (Lin Jian-Feng)
# Email: designer@calvinlam.top
# Website: calvinlam.top

import socket
import threading

import re

import serial
ser = serial.Serial("COM12",9600)


patt=r'i'
patt1=r'I'

def clientThreadIn(conn,nick): 
    global data
    while True:
        try:
            temp = conn.recv(1024)#客户端发过来的消息
            if not temp:
                conn.close()
                return
            NotifyAll(temp)
            m = re.search(patt, data.decode('utf-8'))
            dataTemp = re.sub(patt, "*", data.decode('utf-8'))
            mm = re.search(patt1, dataTemp)
            print(re.sub(patt1, "*", dataTemp))
            if m != None or mm != None:
                ArduinoFuntion()
            else:
                CloseArduinoFuntion()




        except:
            NotifyAll('--- ' + nick+' '+'leaves the room ---')#出现异常就退出
            print(data)
            return

def ArduinoFuntion():
    ser.write(b'126')


def CloseArduinoFuntion():
    ser.write(b'')

    


def clientThreadOut(conn,nick):
    global data
    while True:
        if con.acquire():
            con.wait()#堵塞，放弃对资源的占有  等待通知运行后面的代码
            if data:
                try:
                    conn.send(data)
                    con.release()
                except:
                    con.release
                    return


def NotifyAll(ss):
    global  data
    if con.acquire():#获取锁
        data = ss
        con.notifyAll()#当前线程放弃对资源的占有，通知所有等待x线程
        con.release()


con = threading.Condition()#条件
Host = input('input the server ip address:')# ip地址
port = 1111
data = ''


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#创建套接字
print('Socket created')
s.bind((Host,port)) #把套接字绑定到ip地址
s.listen(5)
print('Socket now listening')

while True:
    conn,addr = s.accept()#接受连接
    print('Connected with '+'' +addr[0]+':'+str(addr[1])) #字符串拼接
    nick = conn.recv(1024)#获取用户名
    nick = nick.decode("utf-8")
    NotifyAll('--- Welcome'+' '+nick+' to the room! ---')
    print(data)
    print(str(int((threading.activeCount()+1)/2))+' person(s)')
    data = data.encode("utf-8")
    conn.sendall(data)
    threading.Thread(target=clientThreadIn,args=(conn,nick)).start()
    threading.Thread(target=clientThreadOut,args=(conn,nick)).start()

