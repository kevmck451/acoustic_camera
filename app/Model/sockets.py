


import socket

# Functions to setup things to use the sockets
# like bash scripts for ssh
# ssh key-based authentication needs to be set up
# if start_fpga_server.sh doesnt exist, create it


class EventListenerSocket:
    def __init__(self):
        self.host = None
        self.port = None
        self.sock = None

    def start_EL_connection(self):

        self.sock.connect()

class VideoFeedSocket:
    def __init__(self):
        pass



# Socket used for communicating to mics
class FPGASocket:
    def __init__(self, host, port, MSGLEN, sock=None):
        self.host = host
        self.port = port
        self.MSGLEN = MSGLEN
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self):
        self.sock.connect((self.host, self.port))

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < self.MSGLEN:
            chunk = self.sock.recv(min(self.MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd += len(chunk)
        return b''.join(chunks)

    def close(self):
        self.sock.close()