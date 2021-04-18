from _thread import *
import threading
import socket

print_lock = threading.Lock()

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = str(s.getsockname()[0])
    s.close()
    return ip

def threaded(c,ip):
    while True:
        data = c.recv(1024)
        if not data:
            print('Desconectado',ip)
            print_lock.release()
            break
        print("mensaje ",str(data),"ip:",ip)
        data = data[::-1]
        c.send(data)
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
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        start_new_thread(threaded, (c,addr[0]))
    s.close()

if __name__ == '__main__':
    Main()