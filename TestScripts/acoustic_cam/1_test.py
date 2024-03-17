import socket
import subprocess
import time

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(1)
    connection, client_address = server_socket.accept()

    try:
        player = None
        with connection.makefile('rb') as stream:
            cmdline = ['vlc', '--demux', 'h264', '-']
            player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
            while True:
                data = stream.read(1024)
                if not data:
                    break
                player.stdin.write(data)
                player.stdin.flush()
    finally:
        if player:
            player.terminate()
        connection.close()
        server_socket.close()

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.0.140', 8000)
    client_socket.connect(server_address)

    try:
        with client_socket.makefile('wb') as connection:
            with picamera.PiCamera() as camera:
                camera.resolution = (640, 480)
                camera.framerate = 24
                camera.start_preview()
                time.sleep(2)

                camera.start_recording(connection, format='h264')
                camera.wait_recording(60)
                camera.stop_recording()
    finally:
        client_socket.close()

if __name__ == '__main__':
    mode = input("'s' for server | 'c' for client: ")
    if mode == 's':
        server()
    elif mode == 'c':
        client()




