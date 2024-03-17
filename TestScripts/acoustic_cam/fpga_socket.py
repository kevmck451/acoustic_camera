import socket

class FPGASocket:

    # Initialization method for socket
    def __init__(self, MSGLEN, sock=None):
        if sock is None:
            # AF_INET sets socket connect via internet and SOCK_STREAM specifies TCP
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.MSGLEN = MSGLEN

    # Connect method to connect to host and port
    def connect(self, host, port):
        self.sock.connect((host, port))

    # Send message method
    def mysend(self, msg):
        totalsent = 0 # Variable describing how much of a message has been sent
        while totalsent < self.MSGLEN:
            sent = self.sock.send(msg[totalsent:]) # Send msg from index totalsent to end, returns indices sent
            if sent == 0: # If 0 indices/bytes sent, must mean connection is broken
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent # Add the number of indices sent to totalsent, so that msg can be resent starting
                                         #  from index last sent

    # Receive message method
    def myreceive(self):
        # Initialize chunks array and bytes received as empty and 0, respectively.
        chunks = []
        bytes_recd = 0
        while bytes_recd < self.MSGLEN: # While bytes received < message length
            # Set socket to receive a message of size MSGLEN - bytes_recd or 2048
            #   so that the chunk is no larger than 2048 bytes (a buffer size)
            # 'chunk' is the actual received data.
            chunk = self.sock.recv(min(self.MSGLEN - bytes_recd, 2048))

            if chunk == b'': # If chunk is empty (meaning nothing received), socket must have lost connection.
                raise RuntimeError("socket connection broken")
            chunks.append(chunk) # Add to chunks array to build up the message
            bytes_recd = bytes_recd + len(chunk) # Incremenet the number of bytes received
        return b''.join(chunks) # Return a binary representation of the message where all pieces/chunks are joined into one message.