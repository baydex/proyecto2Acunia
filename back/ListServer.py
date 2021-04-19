import socket
import json
import time
import threading
import psycopg2

users = {}

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

def dic_keys_bytes(data):
    flagUsers = {}
    for i in users:
        flagUsers[i] = users[i][1]
    return json_bytes(flagUsers)

def hilo(c,ip):  #abrimos un hilo para verificar que siga activo el usuario
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

def send_to_all(users): # Enviar lista de usuarios a todos activos
    for i in users:
        users[i][0].send(dic_keys_bytes(users))

def conexionBD():  # coneccion a la base de datos acunia
    conexion1 = psycopg2.connect(
        database = "acunia",
        user = "acunia",
        password = "soyacunia"
    )
    return conexion1

def autenticacion(auth):
    user = auth["user"]
    password = auth["password"]
    option = auth["option"]
    check = False

    conexion = conexionBD()
    if option == "1":
        sql = "select * from users where usuario = '%s' and password = '%s'"%(user,password)
        num = 0
        cursor = conexion.cursor()
        cursor.execute(sql)
        for i in cursor:
            num+=1
        if num == 1:
            check = True
    else:
        sql = "select * from users where usuario = '%s'"%user
        num = 0
        cursor = conexion.cursor()
        cursor.execute(sql)
        for i in cursor:
            num+=1
        if num == 0:
            sql = "insert into users values (%s,%s,%s)"
            data = (user, password, 1)
            cursor = conexion.cursor()
            cursor.execute(sql,data)
            conexion.commit()
            check = True
    conexion.close()
    return check

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
        auth = bytes_json(c.recv(1024))
        name = auth["user"]
        auth = autenticacion(auth)
        c.send(b'1' if auth else b'0')
        if auth:
            print('Connected to :', addr[0], ':', addr[1])
            users[addr[0]] = [c, name ]
            print(dic_keys_bytes(users))
            send_to_all(users)
            threading.Thread(target=hilo
                                ,args=(c, addr[0])).start()
    s.close()

if __name__ == '__main__':
    Main()