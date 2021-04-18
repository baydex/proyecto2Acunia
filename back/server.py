import threading
import socket
import json

users = {}

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = str(s.getsockname()[0])
    s.close()
    return ip

def threaded(c,ip):
    c.send(bytes(ip, 'ascii'))
    while True:
        data = c.recv(1024)
        data = data.decode("ascii")
        data = json.loads(data)
        if not data:
            print('Desconectado',ip)
            break
        print("mensaje ",data,"ip:",ip)
        for i in users:
            users[i].send(bytes(data["message"], "ascii"))
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
        print("ajua")
        try:
            c, addr = s.accept()
            print('Connected to :', addr[0], ':', addr[1])
            threading.Thread(target=threaded
                            ,args=(c,addr[0])).start()
            users[addr[0]] = c
        except:
            pass
    s.close()

if __name__ == '__main__':
    Main()