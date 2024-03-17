


import numpy as np
import socket

class FPGASocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def receive_chunk(self, chunk_size):
        chunk = self.sock.recv(chunk_size)
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        return chunk

    def close(self):
        self.sock.close()



def continuously_receive_data(host, port, cube_rows, cube_cols, element_size):
    cube_size = cube_rows * cube_cols * element_size
    sock = FPGASocket()
    sock.connect(host, port)

    try:
        buffer = b''
        while True:
            buffer += sock.receive_chunk(cube_size)

            while len(buffer) >= cube_size:
                # Extract the first cube from the buffer
                data_cube_bytes = buffer[:cube_size]
                buffer = buffer[cube_size:]

                # Convert the bytes to a numpy array and reshape to 5x5
                cube = np.frombuffer(data_cube_bytes, dtype=np.int16).reshape(cube_rows, cube_cols)
                print(f"Received data cube with shape: {cube.shape}")
                # Process the cube here

    except KeyboardInterrupt:
        print("Stopping data reception.")
    finally:
        sock.close()

if __name__ == '__main__':
    host = '192.168.80.1'  # USB
    port = 2048
    continuously_receive_data(host, port, cube_rows=5, cube_cols=5, element_size=2)
