#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading

sock = socket.socket()
sock.connect(('localhost', 9999))
name = input('input ouyr name:')

def str_json_reg(name):
    St = '{"name":"' + name + '","message":""}<end>'
    StJson = St.replace(' ', ';').replace("'", '"')
    return StJson

def str_json_mes(name, mes):
    St = '{"name":"' + name + '","message":"'+ mes+'"}<end>'
    StJson = St.replace(' ', ';').replace("'", '"')
    return StJson

data = str_json_reg(name)
sock.send(data.encode())

def send():
    while True:
        print('>')
        mes = input()
        print('mes=', mes)
        print(str_json_mes(name, mes))
        sock.send(data.encode())

def get():
    while True:
        data = sock.recv(1024)
        #sock.close()
        print(data.decode())



t_send = threading.Thread(target=send)
t_get = threading.Thread(target=get)
t_send.start()