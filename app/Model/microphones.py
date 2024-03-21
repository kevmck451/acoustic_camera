


import numpy as np


# Local Imports
from .socket_fpga import FPGASocket



class MicArray:
    def __init__(self):
        # this is all specific to the FPGA design
        self.map_row, self.map_col = 5, 5
        self.sample_rate = 48000
        self.sample_length = 0.5  # Half a second
        self.host = '192.168.80.1'
        self.port = 2048
        self.buffer_size = 2 * self.map_row * self.map_col * int(self.sample_rate * self.sample_length)
        self.sock = None

    def start_client_connection(self):
        self.sock = FPGASocket(self.host, self.port, self.buffer_size)
        self.sock.connect()

    def end_client_connection(self):
        self.sock.close()

    def receive_data_cube(self):
        N = int(self.sample_rate * self.sample_length)
        data = self.sock.myreceive()
        cube = np.frombuffer(data, dtype=np.int16).reshape(-1, self.map_row, self.map_col)
        return cube

    def get_RMS(self):
        print('Starting RMS Calcuation'+'-'*20)
        while True:
            print('Running')
            cube = self.receive_data_cube()
            rms_values = np.zeros((self.map_row, self.map_col))

            for i in range(self.map_row):
                for j in range(self.map_col):
                    square_data = cube[:, i, j]
                    rms = np.sqrt(np.mean(square_data ** 2))
                    rms_values[i, j] = rms

            print("RMS values for each square in the cube:")
            print(rms_values)
            print('-' * 50)

            return rms_values


