import numpy as np
import socket

import matplotlib
# matplotlib.use('TkAgg')  # Set the backend to TkAgg
matplotlib.use('Agg')  # Set the backend to TkAgg
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

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

def receive_data_cube(sock, map_row, map_col, sample_rate, sample_length):
    N = int(sample_rate * sample_length)
    data = sock.myreceive()
    cube = np.frombuffer(data, dtype=np.int16).reshape(-1, map_row, map_col)
    return cube

def update_heatmap(ax, data, vmin=30, vmax=100):
    ax.clear()
    ax.imshow(data, cmap='Reds', alpha=0.3, vmin=vmin, vmax=vmax)
    plt.draw()

if __name__ == '__main__':
    map_row, map_col = 5, 5
    sample_rate = 48000
    sample_length = 0.5  # Half a second
    host = '192.168.80.1'
    port = 2048
    rms_threshold = 20
    rms_max = 80

    buffer_size = 2 * map_row * map_col * int(sample_rate * sample_length)
    sock = FPGASocket(host, port, buffer_size)
    sock.connect()

    fig, ax = plt.subplots()
    ax.set_xlim(0, map_col)
    ax.set_ylim(0, map_row)
    plt.show(block=False)

    try:
        while True:
            cube = receive_data_cube(sock, map_row, map_col, sample_rate, sample_length)
            rms_values = np.zeros((map_row, map_col))

            for i in range(map_row):
                for j in range(map_col):
                    square_data = cube[:, i, j]
                    rms = np.sqrt(np.mean(square_data ** 2))
                    rms_values[i, j] = rms

            update_heatmap(ax, rms_values, rms_threshold, rms_max)
            plt.pause(0.05)
            print("RMS values for each square in the cube:")
            print(rms_values)
            print('-' * 50)

    except KeyboardInterrupt:
        print("Stopping cube reception.")
    finally:
        sock.close()
