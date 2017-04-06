import socket
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 1154))

def send_mes():
    while True:
       print("Щоб вийт нажміть 'exit':")
       print("Введіть повідомлення")
       data = input()
       if (data != 'exit'):
           client_socket.send(data.encode())
           data = client_socket.recv(1024)
           print(data.decode())
       else:
           client_socket.send(data.encode())
           client_socket.close()
           break

tsend = threading.Thread(target=send_mes())
tsend.start()
tsend.join()