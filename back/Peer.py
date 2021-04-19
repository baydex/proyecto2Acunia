import socket
import json
import threading
import time


user_list = dict()

def getIP(): # Obtengo mi ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = str(s.getsockname()[0])
    s.close()
    return ip

def json_bytes(data):
    return bytes( json.dumps(data)   , "ascii")

def bytes_json(data):
    return json.loads(data.decode("ascii"))

def connectListServer(option):
    user = input("Ingresa el nombre de usuario\n")
    password = input("Ingresa la contraseña\n")
    autentication = False

    host = '10.0.0.19' # IP del servidor de lita de IPs
    port = 54321        #Puerto random
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    auth = {"user": user,
            "password": password,
            "option": option}
    auth = json_bytes(auth)
    s.send(auth)
    auth = s.recv(1024).decode("ascii")
    if auth == '1':
        threading.Thread(target=menu).start()
        try:
            while True:
                data = s.recv(1024)
                # print('Received from the server :', data.decode('ascii'))
                global user_list
                user_list = bytes_json(data)
                user_list = dict(filter(lambda x: x[0] != getIP(), user_list.items()))
        except KeyboardInterrupt:
            s.send(b'')
            s.close()
    else:
        print("Credenciales invalidas")
        s.close()

def writer(ip_dest):
    pass


def menu():
    threading.Thread(target=writer, args=ip_dest).start() #Un hilo se conecta al servidor de listas de IPs
    threading.Thread(target=listener, args=ip_dest).start() #Un hilo se conecta al servidor de listas de IPs


def Main():
    flag = True
    while(flag):
        option = input("Selecciona una opcion\n1=Login\n2=Registro\n")
        if option == "1" or option == "2":
            threading.Thread(target=connectListServer, args=option).start() #Un hilo se conecta al servidor de listas de IPs
            flag = False
        else:
            print("Ingresa una opcion valida")
    
    

if __name__ == '__main__':
    Main()