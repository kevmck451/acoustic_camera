
# Local Imports
from app.Model.pi_hardware.socket_fpga import FPGASocket


import numpy as np



class MicArray:
    def __init__(self):
        # this is all specific to the FPGA design
        self.map_row, self.map_col = 5, 5
        self.sample_rate = 48000
        self.sample_length = 0.05  # 0.05 to 0.5
        self.host = '192.168.80.1'
        self.port = 2048
        self.buffer_size = 2 * self.map_row * self.map_col * int(self.sample_rate * self.sample_length)
        self.sock = None
        self.RMS_values = np.zeros((self.map_row, self.map_col))
        self.running = True

    def __str__(self):
        return f'Passive Acoustic Phase Array'

    def start_client_connection(self):
        self.sock = FPGASocket(self.host, self.port, self.buffer_size)
        self.sock.connect()

    def end_client_connection(self):
        self.sock.close()

    def receive_data_cube(self):
        # N = int(self.sample_rate * self.sample_length)
        data = self.sock.myreceive()
        cube = np.frombuffer(data, dtype=np.int16).reshape(-1, self.map_row, self.map_col)
        return cube

    def get_RMS(self):

        while self.running:
            cube = self.receive_data_cube()

            for i in range(self.map_row):
                for j in range(self.map_col):
                    square_data = cube[:, i, j]
                    mean_square = np.mean(square_data ** 2)
                    # Check if mean_square is non-zero (or has changed)
                    if mean_square > 0: rms = np.sqrt(mean_square)
                    else: rms = 0
                    self.RMS_values[i, j] = rms

            # for i in range(self.map_row):
            #     for j in range(self.map_col):
            #         square_data = cube[:, i, j]
            #         rms = np.sqrt(np.mean(square_data ** 2))
            #         self.RMS_values[i, j] = rms

            # print('RMS values for each square in the cube:')
            # print(self.RMS_values)
            # print(f'Max: {int(np.round(np.max(self.RMS_values)))} | min: {int(np.round(np.min(self.RMS_values)))}')
            # print('-' * 69)

    def stop(self):
        self.running = False
