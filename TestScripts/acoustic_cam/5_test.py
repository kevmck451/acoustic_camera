import numpy as np
import socket
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

def update_heatmap(fig, ax, data):
    ax.clear()
    norm = mcolors.Normalize(vmin=30, vmax=100)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            color = np.array([1.0, 0, 0, min(max(data[i, j] / 100, 0.3), 1.0)])
            rect = plt.Rectangle((j, data.shape[0] - i - 1), 1, 1, color=color)
            ax.add_patch(rect)
    plt.pause(0.05)

if __name__ == '__main__':
    map_row, map_col = 5, 5
    sample_rate = 48000
    sample_length = 0.5  # Half a second
    host = '192.168.80.1'
    port = 2048
    max_cubes = 10

    buffer_size = 2 * map_row * map_col * int(sample_rate * sample_length)
    sock = FPGASocket(host, port, buffer_size)
    sock.connect()

    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlim(0, map_col)
    ax.set_ylim(0, map_row)

    try:
        while True:
            cube = receive_data_cube(sock, map_row, map_col, sample_rate, sample_length)
            rms_values = np.zeros((map_row, map_col))

            for i in range(map_row):
                for j in range(map_col):
                    square_data = cube[:, i, j]
                    rms = np.sqrt(np.mean(square_data ** 2))
                    rms_values[i, j] = rms

            update_heatmap(fig, ax, rms_values)
            print("RMS values for each square in the cube:")
            print(rms_values)
            print('-' * 50)

    except KeyboardInterrupt:
        print("Stopping cube reception.")
    finally:
        sock.close()
        plt.ioff()
        plt.show()
