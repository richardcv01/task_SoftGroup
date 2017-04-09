#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
import json

import msvcrt
import sys

sock = socket.socket()
sock.connect(('localhost', 9999))

def str_json_reg(name):
    St = '{"name":"' + name + '","message":""}<end>'
    StJson = St.replace("'", '"')
    return StJson



def str_json_mes(name, mes):
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
        print('>>>', end ='')
        mes = input()
        #print('mes=', mes)
        #print(str_json_mes(name, mes))
        data = str_json_mes(name, mes)
        sock.send(data.encode())

def get():
    while True:
        print('>', end ='')
        try:
            data_get = b''
            while True:
                data_get = data_get +  sock.recv(10)
                #print('data   ', data_get)
                if data_get.decode()[-5:] == '<end>':
                    #print(data_get)
                    break
                #print(data_get)
        #sock.close()
            print('GET', data_get)
            name, mes = json_name_mes(data_get.decode())
            if name == mes == '':
                pass
            else:
                print(name, ':', mes)
        except ConnectionResetError:
            print('Disconected from chatroom. Press <enter to exit>')
            while True:
                key = msvcrt.getch()  # Какая клавиша нажата?
                print('ker', key)
                if key == 13:  # если Enter:
                    print(key)
                    raise SystemExit

name = ''
def register():
    global name
    while name == '':
        try:
            name = input('Input your name: ')
            #if name != '': break
            data = str_json_reg(name)
            sock.send(data.encode())
            data_get = sock.recv(1024)
            sername, mes = json_name_mes(data_get.decode())
            if  mes == "Name <" + name + "> is alredy taken. Choose another name":
                name = ''
            if sername == mes == '':
                pass
            else:
                print(sername, ':', mes)
        except ConnectionResetError:
            print('Disconected from chatroom. Press <enter to exit>')
            while True:
                key = msvcrt.getch()  # Какая клавиша нажата?
                print('ker', key)
                if key == 13:  # если Enter:
                    print(key)
                    raise SystemExit


register()

t_send = threading.Thread(target=send)
t_get = threading.Thread(target=get)
t_get.start()
t_send.start()

