import socket
from threading import Thread, current_thread
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'
port = 9999
LIST_NAME_USER = []

sock.bind((host, port))
sock.listen(5)

print("<server debug>")
print(''.join(['Server starter on ',host,':', str(port)]))

running = True

def clientthread(conn):
    while True:
        #running
        print(str(conn))
        buf = conn.recv(1024)
        data = register(buf.decode())
        conn.send(data.encode())
        if data[-5:] =='<end>':
            break

def register(jsonSt):
    dictjson = json.loads(jsonSt[:-5], object_pairs_hook=dict)

    if dictjson["name"] != '' and dictjson["message"] == '':
        if dictjson["name"] in LIST_NAME_USER:
            return 'Name "' + dictjson["name"] + '" is alredy taken'
        else:
            LIST_NAME_USER.append(dictjson["name"])
            return 'Welcome to chat, ' + dictjson["name"]
    elif dictjson["name"] == '' :
        return 'Need to introdusce yourself'




while True:
    if running:
        conn, addr = sock.accept()
        print("client connected with address " + addr[0] + str(conn))
        #conn.send(b"hello!")
        ht = Thread(target=clientthread, args=(conn,))
        ht.daemon = True
        ht.start()
        print(running)
    else:
        break





conn.close()
sock.close