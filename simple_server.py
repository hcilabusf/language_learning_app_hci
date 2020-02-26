# Python program to implement server side of chat room.
import socket
from _thread import start_new_thread
import threading
import os
import datetime

class SocketServer:
    def __init__(self, ip, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((ip, port))
        server.listen(5)
        self.server = server
        self.list_of_clients = []

    """ Thread for new client """
    def client_thread(self, conn, addr, i):
        # sends a message to the client whose user object is conn
        conn.send('Welcome to this chatroom!'.encode())
        while True:
            try:
                message = conn.recv(1024).decode()
                if message:
                    # Calls broadcast function to send message to all
                    message_to_send = "<" + addr[0] + "> " + message
                    #TODO add thread number  in the future
                    date_object = datetime.date.today()
                    filename = 'Thread' + str(i) + '_' +str(date_object)
                    print(str(i) + ' - msg to write: [' + message_to_send + ']')
                    with open(filename, "a") as myfile:
                        myfile.write(message_to_send)
                        myfile.write('\n')

                else:
                    self.remove(conn)
                    print("Disconnecting, %d", i)
                    break

            except Exception as e:
                print("Exception: %s" % str(e))
                continue

    """ Remove a sockets connection """
    def remove(self, connection):
        if connection in self.list_of_clients:
            self.list_of_clients.remove(connection)

    """ Accept new socketes connections """
    def accept_connections(self):
        i = 0
        while True:
            print('...in the connecting- start of true while loop')
            conn, addr = self.server.accept()

            self.list_of_clients.append(conn)

            # prints the address of the user that just connected
            print(addr[0] + " connected")

            # creates and individual thread for every user that connects
            process = threading.Thread(target=self.client_thread, args=[conn, addr, i])

            print('starting a new thread')
            print('\tth_name: ' + process.name)
            process.start()
            i += 1


def main():
    server = SocketServer("127.0.0.1", 8080)
    server.accept_connections()
    print('end of main')


if __name__ == "__main__":
    main()
