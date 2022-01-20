import socket
import time, sys
from multiprocessing import Process

from echo_server import BUFFER_SIZE

HOST = ''
PORT = 8001
BUFFER_SIZE = 1024

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()
    print(f'IP address of {host} is {remote_ip}')
    return remote_ip


def main():
    host = 'www.google.com'
    port = 80
    # create socket, bind, and set to listening mode
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Starting proxy server")
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(2)

        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)

            # act as a client -> send data from client to server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(host)

                # connect to Google at http port
                proxy_end.connect((remote_ip, port))
                p = Process(target=handle_request, args=(addr, conn, proxy_end))
                p.daemon = True
                p.start()
                print("Started process ", p)
            conn.close()

def handle_request(addr, conn, proxy_end):
    send_full_data = conn.recv(BUFFER_SIZE)  # get data from client
    print(f"Sending received data {send_full_data} to google")
    proxy_end.sendall(send_full_data) # then send to google
    proxy_end.shutdown(socket.SHUT_WR)

    data = proxy_end.recv(BUFFER_SIZE) # get data from google
    print(f'Sending received data {data} to client')
    conn.send(data) # send data to client

if __name__ == "__main__":
    main()