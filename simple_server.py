# Python program to implement server side of chat room.
import socket
from _thread import start_new_thread
import threading
import os

class SocketServer:
    def __init__(self, ip, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((ip, port))
        server.listen(5)
        self.server = server
        self.list_of_clients = []

    """ Thread for new client """
    def client_thread(self, conn, addr):
        # sends a message to the client whose user object is conn
        
        conn.send('Welcome to this chatroom!'.encode())
        while True:
            try:
                message = conn.recv(1024).decode()
                if message:

                    # Calls broadcast function to send message to all
                    message_to_send = "<" + addr[0] + "> " + message        
                    print('msg to send: [' + message_to_send + ']')
                    with open("tempfile", "a") as myfile:
                        myfile.write(message_to_send)
                        myfile.write('\n')            
#                    self.broadcast(message_to_send)
                    f.close()          
                else:
                    self.remove(conn)
                    break

            except Exception:
                continue


#    """ Broadcast a message to all connected clients"""
#    def broadcast(self, message):
#        #print("ALL connections: %s" % self.list_of_clients)
#        print("\nBroadcast: Number of connections: %s" % len(self.list_of_clients))
#        for clients in self.list_of_clients:
#            try:
#                print("Sending %s to: %s" % (message, clients))
#                clients.send(message.encode())
#            except Exception:
#                clients.close()
#                self.remove(clients)


    """ Remove a sockets connection """
    def remove(self, connection):
        if connection in self.list_of_clients:
            self.list_of_clients.remove(connection)

    """ Accept new socketes connections """
    def accept_connections(self):
        while True:
            print('...in the connecting- start of true while loop')
            conn, addr = self.server.accept()

            self.list_of_clients.append(conn)

            # prints the address of the user that just connected
            print(addr[0] + " connected")

            # creates and individual thread for every user that connects
            process = threading.Thread(target=self.client_thread, args=[conn, addr])
            process.start()


def main():
    server = SocketServer("127.0.0.1", 8080)
    server.accept_connections()
    print('end of main')


if __name__ == "__main__":
    main()
