import socket
import json
import time
import threading

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
    flagUsers = {}
    for i in users:
        flagUsers[i] = users[i][1]
    return json_bytes(flagUsers)

def threaded(c,ip):
    try:
        while True:
            data = c.recv(1024)
            if not data:
                print('Desconectado',ip)
                users.pop(ip)
                send_to_all(users)
                break
    except:
        print('Desconectado',ip)
        users.pop(ip)
        send_to_all(users)
        c.close()

def send_to_all(users):
    for i in users:
        users[i][0].send(dic_keys_bytes(users))

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
        name = c.recv(1024).decode("ascii")
        users[addr[0]] = [c, name ]
        print(users)
        send_to_all(users)
        threading.Thread(target=threaded
                            ,args=(c, addr[0])).start()
    s.close()

if __name__ == '__main__':
    Main()