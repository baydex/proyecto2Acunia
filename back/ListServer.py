from _thread import *
import threading
import socket
import json
import time

users = {}

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = str(s.getsockname()[0])
    s.close()
    return ip

def json_bytes(data):
    return bytes( json.dumps(data)   , "ascii")

def bytes_json(data):
    return json.loads(data.decode("ascii"))

def dic_keys_bytes(data):
    keys = lambda x: [i for i in x]
    return bytes(str(keys(data)), "ascii")

def threaded(c,ip):
    while True:
        pass
    c.close()

def Main():
    
    host = getIP()
    port = 54321
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Servidor alojado en", host)
    print("Con el puerto", port)
    s.listen(5)
    print("Esperando solicitudes")
    while True:
        c, addr = s.accept()
        print('Connected to :', addr[0], ':', addr[1])
        users[addr[0]] = c
        threading.Thread(target=threaded
                        ,args=(c,addr[0])).start()
        for i in users:
            users[i].send(dic_keys_bytes(users))
    s.close()

if __name__ == '__main__':
    Main()