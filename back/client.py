import socket
def Main():
    host = '10.0.0.10'
    port = 54321
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    while True:
        message = input("Escribe un mensaje\n")
        if message == '':
            break
        s.send(message.encode('ascii'))
        data = s.recv(1024)
        print('Received from the server :',str(data.decode('ascii')))
    s.close()
  
if __name__ == '__main__':
    Main()