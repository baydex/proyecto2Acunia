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
  
        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')
              
            # lock released on exit
            print_lock.release()
            break
        print("mensaje ",str(data),"ip:",ip)
        # reverse the given string from client
        data = data[::-1]
  
        # send back reversed string to client
        c.send(data)
  
    # connection closed
    c.close()

def Main():
    host = getIP()
  
    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
    print("socket at host", host)
  
    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
  
    # a forever loop until client wants to exit
    while True:
  
        # establish connection with client
        c, addr = s.accept()
  
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
  
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,addr[0]))
    s.close()
  
  
if __name__ == '__main__':
    Main()