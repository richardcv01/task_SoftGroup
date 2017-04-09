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
    def __init__(self, conn, adrr):
        threading.Thread.__init__(self)
        self.daemon = True
        self.conn = conn
        self.addr = adrr
        self.REGIS = False

    def run(self):
        conn = self.conn
        while True:
            # running
            #print(self.REGIS, self.conn)
            if self.REGIS == False:
                buf = b''
                while True:
                    buf = buf + conn.recv(10)
                    if (buf.decode()[-5:]) == '<end>':
                        break
                #buf = conn.recv(10)
                data = self.register(buf.decode())
                mes = self.str_json_mes(data)
                name, mess = self.json_name_mes(buf.decode())
                conn.send(mes.encode())
            else:
                buf = b''
                while True:
                    buf = buf + conn.recv(10)
                    if (buf.decode()[-5:]) == '<end>':
                        break
                name, mes = self.json_name_mes(buf.decode())
                conn.send(mes.encode())
                #if buf
                dictjson = json.loads(buf.decode()[:-5], object_pairs_hook=dict)
                if 'to' in dictjson:
                    user = dictjson['to']
                    if user in ClientThread.user:
                        sock = ClientThread.user[user]
                        print('!!!!!!!!!!!!!!!1',sock)
                        print(buf)
                        name, messag = self.json_name_mes(buf.decode())
                        St = '{"name":"'+name+'","message":"' + mes + '"}<end>'
                        StJson = St.replace("'", '"')
                        print(St)
                        sock.send(St.encode())

                else:
                    for addr, sock in ClientThread.sockets.items():
                        if addr != self.addr and sock != self.conn:
                            print(buf)
                            sock.send(buf)

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
                ClientThread.sockets[self.addr] = self.conn
                ClientThread.user[self.user] = self.conn
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
        conn, addr = sock.accept()

        print("client connected with address " + addr[0] + str(conn))
        t = ClientThread(conn, addr)
        t.start()
        #print(LIST_THREDS)
    else:
        break

conn.close()
sock.close