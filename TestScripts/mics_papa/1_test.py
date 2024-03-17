


import numpy as np
import socket
import time

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



if __name__ == '__main__':
    while True:
        map_row, map_col = 5, 5

        sample_rate = 48000
        sample_length = 2  # In seconds

        host = '192.168.80.1'  # USB
        port = 2048
        N = sample_rate * sample_length

        sock = FPGASocket(map_row * map_col * 2 * N)
        sock.connect(host, port)

        # Socket set to receive data
        data = sock.myreceive()

        # frombuffer takes the received data (from socket_test)
        #   and puts it into an array, viewing the data as 16-bit ints rather than
        #   unsigned 8-bit ints. The reshape function then takes the created array
        #   and turns it into a 48000x7x7 data cube (-1 serves as a "fill-in" number
        #   as the program can tell how the elements divide into a 7x7 size. So, since
        #   the matrix size is 7x7 (x, 7, 7), it can tell that the total message length
        #   will be able to fit into 48000 layers, like defined in Line 43. This means
        #   that 49*2*48000 implicitly chooses the number of matrices).
        cube = np.frombuffer(data, dtype=np.int16).reshape(-1, map_row, map_col)
        print(cube.shape)

        # Close socket
        print("closing")
        # sock.sock.shutdown(socket.SHUT_RDWR)
        sock.sock.close()
        sock = None

        """
        cube = np.load(f'/Users/noahd/Desktop/EECE4280/Data Cube Samples/Synthetic/PAPA Test Cubes/Test_Cube_{i}.npy')
        #print(cube)
        #cube = np.transpose(cube, (2, 0, 1))
        #cube = cube[:N, :, :]"""
        print(cube.shape)


        # feature_maps = extract_features(cube, map_row, map_col, power_threshold, feature_type[0], feature_params_mfcc, sample_rate, processes)


        # time.sleep(1)

        try:
            pass
        except KeyboardInterrupt:
            print("Stream stopped")