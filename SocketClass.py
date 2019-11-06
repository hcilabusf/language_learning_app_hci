import socket

class Socket_Class():

    listening = True

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.allDataReceived = []

    """
    A function that opens a socket with Matlab PC
    """
    def openSocket(self):
        try:
            self.sockett = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return True
            #connected = self.sockett.connect((self.host, self.port))
        except Exception as e:
            print("Error creating socket, %s" % str(e))
            return False

    """
    function that sends data throught the socket to Matlab PC
    """
    def sendData(self, data):
        try:
            self.sockett.sendall(data.encode('utf-8')) # send marker data to Matlab PC
        except Exception as e:
            print(e)

    """
    Get method that returns allDataRecieved list
    """
    def getAllDataReceived (self):
        return self.allDataReceived

    """
    A function that closes the socket
    """
    def closeSocket(self):
        try:
            self.listening = False
            self.sockett.close()
        except Exception as e:
            print(e)
