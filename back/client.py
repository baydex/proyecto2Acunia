import socket
import json
def Main():
    host = '10.0.0.19'
    port = 6666
    nombre = input("Nombre? \n")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    ip = s.recv(1024).decode('ascii')
    while True:
        message = input("Escribe un mensaje\n")
        if message == '':
            break
        data = {
            "name":ip,
            "message": message,
            "nombre": nombre
        }
        data = bytes(json.dumps(data), 'ascii')
        s.send(data)
        data = s.recv(1024)
        print('Received from the server :', data.decode('ascii'))
    s.close()
  
if __name__ == '__main__':
    Main()