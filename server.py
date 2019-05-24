
import socket
import threading
 
import re

import serial
ser = serial.Serial("COM12",9600)

patt=r'i'
patt1=r'I'


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
#sock.bind(('10.10.10.2', 5550))
sock.bind(('10.10.10.2', 5550))
 
sock.listen(5)
print('Server', socket.gethostbyname('10.10.10.2'), 'listening ...')
 
mydict = dict()
mylist = list()
 
#把whatToSay传给除了exceptNum的所有人
def tellOthers(exceptNum, whatToSay):
    for c in mylist:
        if c.fileno() != exceptNum :
            try:
                c.send(whatToSay.encode())
            except:
                pass
 
def subThreadIn(myconnection, connNumber):
    nickname = myconnection.recv(1024).decode()
    mydict[myconnection.fileno()] = nickname
    mylist.append(myconnection)
    print('CONNECTION', connNumber, 'HAS NICKNAME :', nickname)
    tellOthers(connNumber, '---- WELCOME '+mydict[connNumber]+' TO THE ROOM! ----')
    while True:
        try:
            recvedMsg = myconnection.recv(1024).decode()

            m = re.search(patt, recvedMsg)
            dataTemp = re.sub(patt, "*", recvedMsg)
            mm = re.search(patt1, dataTemp)
            recvedMsg = re.sub(patt1, "*", dataTemp)

            if recvedMsg:
                print(mydict[connNumber], ':', recvedMsg)
                tellOthers(connNumber, mydict[connNumber]+' :'+recvedMsg)

            if m != None or mm != None:
                ArduinoFuntion()
            else:
                CloseArduinoFuntion()
 
        except (OSError, ConnectionResetError):
            try:
                mylist.remove(myconnection)
            except:
                pass
            print(mydict[connNumber], 'EXIT, ', len(mylist), ' PERSON(S) LEFT')
            tellOthers(connNumber, '---- '+mydict[connNumber]+' LEAVES THE ROOM ----')
            myconnection.close()
            return

def ArduinoFuntion():
    ser.write(b'126')


def CloseArduinoFuntion():
    ser.write(b'')

 
while True:
    connection, addr = sock.accept()
    print('Accept a new connection', connection.getsockname(), connection.fileno())
    try:
        #connection.settimeout(5)
        buf = connection.recv(1024).decode()
        if buf == '1':
            connection.send(b'WELCOME TO CHAT ROOM!')
 
            #为当前连接开辟一个新的线程
            mythread = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))
            mythread.setDaemon(True)
            mythread.start()
            
        else:
            connection.send(b'please go out!')
            connection.close()
    except :  
        pass
