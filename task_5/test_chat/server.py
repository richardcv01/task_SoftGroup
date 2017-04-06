import socket
import time
import json
import collections as col
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 1154))
server_socket.listen(5)

print("TCPServer Waiting 1154")



def json_to_str(json_dic):
    dicOrd = json.load(json_dic, object_pairs_hook=col.OrderedDict)
    listRes = dicOrd["rows"]
    stRes = "\n".join(listRes)
    return stRes

def get_con():
    have_connect = 1
    while True:
        client_socket, address = server_socket.accept()
        while have_connect:
            data = client_socket.recv(1024)
            data = data.decode()
            print('від клієнта ', data)
            if (data != 'Q' and data != 'q'):
                print("Відповідь від ", address)
                data = ('online: ' + time.asctime(time.localtime())+ '\n')
                client_socket.send(data.encode())
            else:
               client_socket.close()
               have_connect = 0
               break

def get_new():
  while True:


T1 = threading.Thread(target=get_con)
#T2 = threading.Thread(target=get_con)
#T1.start()
T2.start()
