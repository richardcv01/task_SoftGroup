import socket
import threading
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'
port = 9999
sock.bind((host, port))
sock.listen(100)

print("<server debug>")
print(''.join(['Server starter on ',host,':', str(port)]))

running = True

class ClientThread(threading.Thread):
    LIST_NAME_USER = []
    LIST_USER_CONN = []
    LIST_THREDS = []
    sockets = {}
    user = {}
    def __init__(self, conn_get, conn_send, adrr):
        threading.Thread.__init__(self)
        self.daemon = True
        self.conn_get = conn_get
        self.conn_send = conn_send
        self.addr = adrr
        self.REGIS = False

    def run(self):
        conn_get = self.conn_get
        conn_send = self.conn_send
        while True:
            # running
            #print(self.REGIS, self.conn)
            if self.REGIS == False:
                buf_get = b''
                while True:
                    buf_get = buf_get + conn_get.recv(10)
                    if (buf_get.decode()[-5:]) == '<end>':
                        break
                #buf = conn.recv(10)
                data = self.register(buf_get.decode())
                mes = self.str_json_mes(data)
                name, mess = self.json_name_mes(buf_get.decode())
                conn_send.send(mes.encode())

            else:
                buf_get = b''
                while True:
                    buf_get = buf_get + conn_get.recv(10)
                    if (buf_get.decode()[-5:]) == '<end>':
                        break
                #print("sdfsdf      ",buf_get)
                name, mes = self.json_name_mes(buf_get.decode())
                #conn_send.send(mes.encode())
                #conn_send()
                #if buf
                #print('mes ', mes)
                dictjson = json.loads(buf_get.decode()[:-5], object_pairs_hook=dict)
                if 'to' in dictjson:
                    user = dictjson['to']
                    if user in ClientThread.user:
                        sock_send = ClientThread.user[user]
                        #print('!!!!!!!!!!!!!!!1',sock_send)
                        #print(buf)
                        name, messag = self.json_name_mes(buf_get.decode())
                        St = '{"name":"'+name+'","message":"' + mes + '"}<end>'
                        StJson = St.replace("'", '"')
                        #print(St)
                        sock_send.send(St.encode())

                else:
                    for addr, sock_send in ClientThread.sockets.items():
                        if addr != self.addr and sock.send != self.conn_send:
                            #print(buf_get)
                            #print('send=', sock_send)
                            sock_send.send(buf_get)

    def json_name_mes(self, jsonSt):
        dictjson = json.loads(jsonSt[:-5], object_pairs_hook=dict)
        return dictjson["name"], dictjson["message"]

    def register(self ,jsontSt):
        name, mes = self.json_name_mes(jsontSt)
        if name != '' and mes == '':
            if name in ClientThread.LIST_NAME_USER:
                return "Name <" + name + "> is alredy taken. Choose another name"
            else:
                self.user = name
                ClientThread.LIST_NAME_USER.append(self.user)
                ClientThread.sockets[self.addr] = self.conn_send
                ClientThread.user[self.user] = self.conn_send
                self.REGIS = True
                return 'Welcome to chat, ' + name
        elif name == '':
            return 'Need to introdusce yourself'


    def str_json_mes(self, mes):
        St = '{"name":"Server","message":"' + mes + '"}<end>'
        StJson = St.replace("'", '"')
        return StJson

while True:
    if running:
        conn_get, addr = sock.accept()
        conn_send, addr = sock.accept()

        print("client Get " + addr[0] + str(conn_get))
        print("client Send " + addr[0] + str(conn_send))
        t = ClientThread(conn_get, conn_send, addr)
        t.start()
        #print(LIST_THREDS)
    else:
        break

#conn.close()
#sock.close