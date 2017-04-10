#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
import json
import time
import win32api

sock_set = socket.socket()
sock_set.connect(('localhost', 9999))
sock_get = socket.socket()
sock_get.connect(('localhost', 9999))


def str_json_reg(name):
    St = '{"name":"' + name + '","message":""}<end>'
    StJson = St.replace("'", '"')
    return StJson

def str_json_mes(name, mes):
    if mes[:4] == 'user':

        user = mes.split(sep=' ')[0][5:]
        mes = mes[mes.index(' ', 0, -1):]
        #print(mes)
        St  = '{"name":"' + name + '","message":"'+ mes+'","to":"' + user +'"}<end>'
        #print(St)
    else:
        St = '{"name":"' + name + '","message":"'+ mes+'"}<end>'
    StJson = St.replace("'", '"')
    return StJson

def json_name_mes(jsonSt):
    try:
        dictjson = json.loads(jsonSt[:-5], object_pairs_hook=dict)
        res = dictjson["name"], dictjson["message"]
    except ValueError:
        res  = '',''
    return res

def send():
    while True:
        try:
            mes = ''
            print('>>>', end ='')
            mes = input()
            #print('mes=', mes)
            #print(str_json_mes(name, mes))
            data = str_json_mes(name, mes)
            sock_set.send(data.encode())
            mes = ''
        except ConnectionResetError:
            close_program()

def get():
    while True:
        print('>', end ='')
        try:
            data_get = b''
            while True:
                data_get = data_get +  sock_get.recv(10)
                if data_get.decode()[-5:] == '<end>':
                    break
            name, meseg = json_name_mes(data_get.decode())
            if name == meseg == '':
                pass
            else:
                print(name, ':', meseg)
                    #print('To send data Click Enter')
        except ConnectionResetError:
            close_program()

name = ''
def register():
    global name
    while name == '':
        try:
            name = input('Input your name: ')
            #if name != '': break
            data = str_json_reg(name)
            sock_set.send(data.encode())
            data_get = sock_get.recv(1024)
            sername, mes = json_name_mes(data_get.decode())
            if  mes == "Name <" + name + "> is alredy taken. Choose another name":
                name = ''
            if sername == mes == '':
                pass
            else:
                print(sername, ':', mes)
        except ConnectionResetError:
            close_program()

def close_program():
    while True:
        input('Disconected from chatroom. Press <enter to exit>')
        if win32api.GetAsyncKeyState(13):
            print('program close..')
            time.sleep(1)
            print('...')
            time.sleep(1)
            raise SystemExit()


register()

t_send = threading.Thread(target=send)
t_get = threading.Thread(target=get)
t_get.start()
t_send.start()

