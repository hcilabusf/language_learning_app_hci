# Python program to implement server side of chat room.
import socket
import threading
from threading import current_thread
import datetime

MATLAB_ADDR = "192.168.100"
LANG_APP_ADDR = "192.168.2.200"

class SocketServer:
    def __init__(self, ip, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((ip, port))
        server.listen(5)
        self.server = server
        self.client_dict = {}


    """ Thread for new client """
    def client_thread(self, conn, addr):
        th_name = current_thread().name
        print("in thread, thread name: " + th_name)
        conn.send('Welcome to this chatroom!'.encode())
        while True:
            try:
                message = conn.recv(1024).decode()
                if message:

                    message_to_send = "<" + addr[0] + "> " + message
                    if addr == LANG_APP_ADDR:
                        self.send_msg_to_socket(message, MATLAB_ADDR)

                    date_object = datetime.date.today()
                    filename = th_name + "-" + str(date_object)
                    print(th_name + ' - msg to write: [' + message_to_send + ']')
                    with open(filename, "a") as myfile:
                        myfile.write(message_to_send)
                        myfile.write('\n')

                else:
                    self.remove(addr)
                    print("Disconnecting... %s" % th_name)
                    break

            except Exception as err:
                print("Exception: %s" % str(err))
                continue

    """ Broadcast a message to all connected clients"""
    def send_msg_to_socket(self, message, addr):
        conn = self.client_dict.get(addr, None)
        if conn:
            try:
                conn.send(message.encode())
            except Exception as err:
                print("Exception at send_msg_to_socket error:%s to %s" % (str(err), addr))


    """ Remove a sockets connection """
    def remove(self, addr):
        if addr in self.client_dict.keys():
            del self.client_dict[addr]


    """ Accept new socketes connections """
    def accept_connections(self):
        while True:
            print('...in the connecting- start of true while loop')
            conn, addr = self.server.accept()

            self.client_dict[addr[0]] = conn
            # prints the address of the user that just connected
            print(addr[0] + " connected")

            # creates and individual thread for every user that connects
            thread_item = threading.Thread(target=self.client_thread, args=[conn, addr])

            print('starting a new thread')

            thread_item.start()


def main():
    server = SocketServer("127.0.0.1", 8080)
    server.accept_connections()
    print('end of main')


if __name__ == "__main__":
    main()
