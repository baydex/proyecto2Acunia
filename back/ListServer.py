from _thread import *
import threading
import socket
import time
import json

print_lock = threading.Lock()
users = {}
def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = str(s.getsockname()[0])
    s.close()
    return ip

def threaded(c,ip):
    c.send(bytes(json.dumps(users), 'ascii'))
    while True:
        pass
        # flag = users
        # time.sleep(1)
        # if(flag != users):
        #     c.send(bytes(json.dumps(users), 'ascii'))
    c.close()
    
def Main():
    host = getIP()
    port = 6660
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Servidor alojado en", host)
    print("Con el puerto", port)
    s.listen(5)
    print("Esperando solicitudes")
    while True:
        c, addr = s.accept()
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        start_new_thread(threaded, (c,addr[0]))
        users[addr[0]] = ""
    s.close()
if __name__ == '__main__':
    Main()