from tkinter import messagebox
import socket
import json
import threading
import time
from tkinter import *
from tkinter import ttk


class Aplicacion():
    def __init__(self):
        self.raiz = Tk()
        self.raiz.geometry('400x300')
        self.raiz.configure(bg = 'white')
        self.raiz.title('Aplicación')
        Label(self.raiz, text="Usuarios activos", bg="white").pack(side=TOP, padx=10,pady=10)
        self.UserList = Text(self.raiz, width = 180, height=8, bg="white")
        self.UserList.pack(side=TOP, padx=10,pady=10)
        Label(self.raiz, text="Escribe un usuario al cual conectarte", bg="white").pack(side=TOP, padx=10,pady=5)
        self.UserSelect = ttk.Entry(self.raiz, width=160)
        self.UserSelect.pack(side=TOP, padx=10,pady=5)
        ttk.Button(self.raiz, text="Aceptar", command= lambda: self.connectIP(self.UserSelect.get())).pack(side=TOP, padx=10,pady=5)
        self.login()
        self.raiz.mainloop()
    def updateUsers(self, users):
        usersStr = ""
        for i in users:
            usersStr += users[i] + "\n" 
        self.UserList.delete('1.0', END)
        self.UserList.insert(INSERT, usersStr)
        time.sleep(1)
    def connectIP(self, ip):
        ip = str(ip)
        print(ip)
    def login(self):
        flag = True
        while(flag):
            option = input("Selecciona una opcion\n1=Login\n2=Registro\n")
            if option == "1" or option == "2":
                threading.Thread(target=self.connectListServer, args=option).start() #Un hilo se conecta al servidor de listas de IPs
                flag = False
            else:
                print("Ingresa una opcion valida")
    def writer(self):
        self.wflag = True
        while self.wflag:
            print(user_list)
            self.updateUsers(user_list)

    def listener(self): 
        host = getIP()
        port = 6666
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(5)
        self.c, addr = s.accept()
        flag = messagebox.askyesnocancel(message="Aceptar solicitud de " + str(addr), title="xd")
        if flag:
            self.c.send(bytes(str(addr), "ascii"))
            self.wflag = False
            self.newWindow = Toplevel(self.raiz)
            self.newWindow.geometry('400x300')
            Label(self.newWindow, text="Chat", bg="white").pack(side=TOP, padx=10,pady=10)
            self.Chat = Text(self.newWindow, width = 180, height=8, bg="white")
            self.Chat.pack(side=TOP, padx=10,pady=10)
            Label(self.newWindow, text="Escribe un mensaje", bg="white").pack(side=TOP, padx=10,pady=5)
            self.inputMessage = ttk.Entry(self.newWindow, width=160)
            self.inputMessage.pack(side=TOP, padx=10,pady=5)
            ttk.Button(self.newWindow, text="Aceptar", command= lambda: threading.Thread(target=self.chatListener).start()).pack(side=TOP, padx=10,pady=5)

        else:
            print("rechazado")
    def chatListener(self):
        while True:
            data = self.c.recv(1024).decode("ascii")
            print(data)
            self.Chat.insert(INSERT, data)


    def menu(self):
        self.w = threading.Thread(target=self.writer)
        self.w.start()
        threading.Thread(target=self.listener).start()


    def connectListServer(self,option):
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
            threading.Thread(target=self.menu).start()
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




def Main():
    mi_app = Aplicacion()
    
    
    

if __name__ == '__main__':
    Main()