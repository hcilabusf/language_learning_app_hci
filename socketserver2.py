# Python program to implement server side of chat room.
import socket
from _thread import start_new_thread
import threading

class SocketServer:
    def __init__(self, ip, host):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((ip, host))
        server.listen(5)
        self.server = server
        self.list_of_clients = []

    def clientthread(self, conn, addr):
        # sends a message to the client whose user object is conn
        conn.send("Welcome to this chatroom!".encode())
        while True:
            try:
                message = conn.recv(2048)
                if message:
                    print("<" + addr[0] + "> " + message)

                    # Calls broadcast function to send message to all
                    message_to_send = "<" + addr[0] + "> " + message
                    self.broadcast(message_to_send, conn)
                else:
                    self.remove(conn)

            except Exception:
                continue

    def broadcast(self, message, connection):
        for clients in self.list_of_clients:
            if clients != connection:
                try:
                    clients.send(message)
                except Exception:
                    clients.close()

                    # if the link is broken, we remove the client
                    self.remove(clients)

    def remove(self, connection):
        if connection in self.list_of_clients:
            self.list_of_clients.remove(connection)

    def accept_connections(self):
        while True:
            conn, addr = self.server.accept()
            conn.send("Welcome to this chatroom!".encode())

            self.list_of_clients.append(conn)

            # prints the address of the user that just connected
            print(addr[0] + " connected")

            # creates and individual thread for every user
            # that connects
            #start_new_thread(self.clientthread, (conn, addr))
            threading.Thread(target=self.clientthread, args=((conn, addr)))
