


import socket

# TCP Socket used for communicating to mics
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