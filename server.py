import socket
from threading import Thread

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# AF-INT for ipv4 address
#SOCK_STREAM for TCP protocol
#SOCK_DGRAM from UDP protocol
# AF-INT6 for ipv6 address
ip_address='127.0.0.1'
port=8000
#port can be any number but not a reserved port
server.bind((ip_address,port))
server.listen()
list_of_clients=[]
print("server has started")

def clientThread(conn,addr):
    conn.send("welcome to this chat room".encode('utf-8'))
    while True:
        try:
            message=conn.recv(2048).decode('utf-8')
            if message:
                print ("<" + addr[0] + "> " + message)
                message_to_send = "<" + addr[0] + "> " + message
                broadcast(message_to_send,conn)
            else:
                remove(conn)
        except:
            continue

def broadcast(msg,connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(msg.encode('utf-8'))
            except:
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn,addr = server.accept()
    #it accepts connections and requests by the client and returns conn and address... conn is the socket object whereas addr is a tuple
    list_of_clients.append(conn)
    print(addr[0]+"connected")

    new_thread=Thread(target=clientThread,args=(conn,addr))
    new_thread.start()
    #threading allows different parts of the program to run concurrently where threads are a separate flow of execution

