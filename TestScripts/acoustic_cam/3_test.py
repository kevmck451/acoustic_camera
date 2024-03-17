import numpy as np
import socket


class FPGASocket:
    def __init__(self, MSGLEN, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.MSGLEN = MSGLEN

    def connect(self, host, port):
        self.sock.connect((host, port))

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


def receive_data_cube(host, port, map_row, map_col, sample_rate, sample_length):
    N = sample_rate * sample_length
    buffer_size = 2 * map_row * map_col * N
    sock = FPGASocket(buffer_size)
    sock.connect(host, port)
    data = sock.myreceive()
    sock.close()

    cube = np.frombuffer(data, dtype=np.int16).reshape(-1, map_row, map_col)
    return cube


if __name__ == '__main__':
    map_row, map_col = 5, 5
    sample_rate = 48000
    sample_length = 0.5  # In seconds
    host = '192.168.80.1'  # USB
    port = 2048
    max_cubes = 10  # example limit for received cubes

    cube_count = 0
    while cube_count < max_cubes:
    # while True:
    #     try:
        cube = receive_data_cube(host, port, map_row, map_col, sample_rate, sample_length)
        # print(f"Cube Shape: {cube.shape}")

        # Initialize an empty 2D array for RMS values
        rms_values = np.zeros((map_row, map_col))

        # Calculate RMS for each square in the cube
        for i in range(map_row):
            for j in range(map_col):
                # Extract the data for the current square
                square_data = cube[:, i, j]

                # Calculate RMS of the square
                rms = np.sqrt(np.mean(square_data ** 2))
                rms_values[i, j] = rms

        print("RMS values for each square in the cube:")
        print(rms_values)
        print('-' * 50)

        cube_count += 1

        # except KeyboardInterrupt:
        #     print("Stopping cube reception.")
        #     break
