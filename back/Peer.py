import socket
import json
def Main():
    host = '10.0.0.19'
    port = 6660
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    while True:
        data = s.recv(1024)
        print('Received from the server :',json.loads(data.decode('ascii')))
    s.close()
  
if __name__ == '__main__':
    Main()