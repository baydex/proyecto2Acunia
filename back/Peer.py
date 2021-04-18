import socket
import json
import time
def to_json(data):
    return bytes( json.dumps(data)   , "ascii")

def bytes_json(data):
    return json.loads(data.decode("ascii"))

def Main():
    host = '10.0.0.19'
    port = 54321
    name = input("dime tu nombre\n")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    s.send(bytes(name , "ascii"))
    try:
        while True:
            data = s.recv(1024)
            print('Received from the server :', data.decode('ascii'))
    except KeyboardInterrupt:
        s.send(b'')
        s.close()
  
if __name__ == '__main__':
    Main()